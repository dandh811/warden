from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from apps.users import models
from apps.users import forms
import json
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from apps.users.models import Profile
from django.contrib.auth.hashers import make_password
from apps.article.models import Article, ArticleUser
from utils.notice import WeChatPub
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import datetime
import hashlib
from django.db.models import Q
from loguru import logger


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自Injection博客(www.dongjianjun.com)的注册确认邮件'

    text_content = '''感谢注册小猪哼哼博客！'''

    html_content = '''
                    <p>感谢注册, <a href="https://{}/user/confirm/?code={}" target=blank>确认链接</a>！</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('www.dongjianjun.com', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except Exception as e:
        logger.critical(e)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passwd = request.POST.get('pass')
        repasswd = request.POST.get('repass')
        username = request.POST.get('nickname')
        errors = []
        res = User.objects.filter(email=email)
        if res:
            errors.append('该邮箱已注册！')
        res = User.objects.filter(username=username)
        if res:
            errors.append('该昵称已被人使用！')
        else:
            if passwd != repasswd:
                errors.append("两次输入的密码不一致!")
            else:
                new_user = User.objects.create(email=email, username=username, password=make_password(passwd))
                new_user.save()
                errors = '注册成功，请前往注册邮箱进行验证！'
                code = make_confirm_string(new_user)
                send_email(email, code)

                wechat = WeChatPub()
                title = '【小猪哼哼博客】新用户注册成功通知'
                content = "<div class=\"normal\">新用户注册成功，邮箱名：%s </div>" % email
                wechat.send_msg(title, content)

    return render(request, 'users/register.html', locals())


@csrf_exempt
def email_check(request):
    email = request.POST['email']
    try:
        User.objects.get(email=email)
        msg = 'true'
    except Exception as e:
        msg = 'false'

    return HttpResponse(msg)


@csrf_exempt
def nickname_check(request):
    nickname = request.POST['nickname']
    try:
        User.objects.get(username=nickname)
        msg = 'true'
    except Exception as e:
        msg = 'false'

    return HttpResponse(msg)


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'users/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'users/confirm.html', locals())
    else:
        confirm.user.profile.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'users/confirm.html', locals())


def captcha_refresh(request):
    # 内置的源码
    if not request.is_ajax():
        raise Http404

    new_key = CaptchaStore.pick()
    to_json_response = {
        'key': new_key,
        'image_url': captcha_image_url(new_key),
        # 'audio_url': captcha_audio_url(new_key) if settings.CAPTCHA_FLITE_PATH else None
    }

    return HttpResponse(json.dumps(to_json_response), content_type='application/json')


@csrf_exempt
def login_site(request):
    def current_user_url(user):
        _url = 'article:index'
        # perms = User.get_all_permissions(user)
        # if "article: index" in perms:
        #     _url = "article: index"
        # else:
        #     _url = 'article: index'
        next = request.GET.get('next', None)
        return next and next or reverse(_url)

    if request.method == "POST":
        form = forms.SigninForm(request.POST)
        if form.is_valid():
            human = True
            email = form.cleaned_data['username']
            passwd = form.cleaned_data['password']
            try:
                username = User.objects.get(email=email)
            except Exception as e:
                logger.critical(e)
                username = ''
                errors = '用户不存在！'
            if not username.profile.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'users/login.html', locals())

            user = authenticate(username=username, password=passwd)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(current_user_url(user))
            else:
                errors = u'登陆失败，邮箱或密码错误！'
        else:
            return HttpResponseRedirect(reverse("users:login"))
    else:
        if request.user.is_authenticated:
            url = current_user_url(request.user)
            return HttpResponseRedirect(url)
        else:
            hashkey = CaptchaStore.generate_key()
            image_url = captcha_image_url(hashkey)

            form = forms.SigninForm()

    return render(request, 'users/login.html', locals())


@csrf_exempt
def find_pass(request):
    error = ''
    if request.method == 'POST':
        if request.method == 'POST':
            form = forms.ResetpsdRequestForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                user = get_object_or_404(User, email=email)
                if user:
                    hash_res = hashlib.md5()
                    hash_res.update(make_password(email).encode('utf-8'))
                    urlarg = hash_res.hexdigest()
                    models.UserResetpsd.objects.get_or_create(
                        email=email,
                        urlarg=urlarg
                    )
                    res = mails.sendresetpsdmail(email, urlarg)
                    if res:
                        error = '申请已发送，请检查邮件通知，请注意检查邮箱'
                    else:
                        error = '重置邮件发送失败，请重试'
                else:
                    error = '请检查信息是否正确'
            else:
                error = '请检查输入'
        else:
            form = forms.ResetpsdRequestForm()
        return render(request, 'RBAC/resetpsdquest.html', {'form': form, 'error': error})
    else:
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)

        return render(request, 'users/forget.html', locals())
        # resetpsd = get_object_or_404(models.UserResetpsd,)
        # if resetpsd:
        #     email_get = resetpsd.email
        #     if request.method == 'POST':
        #         form = forms.ResetpsdForm(request.POST)
        #         if form.is_valid():
        #             email = form.cleaned_data['email']
        #             password = form.cleaned_data['password']
        #             repassword = form.cleaned_data['repassword']
        #             if checkpsd(password):
        #                 if password == repassword:
        #                     if email_get == email:
        #                         user = get_object_or_404(User, email=email)
        #                         if user:
        #                             user.set_password(password)
        #                             user.save()
        #                             resetpsd.delete()
        #                             return HttpResponseRedirect('/view/')
        #
        #                         else:
        #                             error = '用户信息有误'
        #                     else:
        #                         error = '用户邮箱不匹配'
        #                 else:
        #                     error = '两次密码不一致'
        #             else:
        #                 error = '密码必须6位以上且包含字母、数字'
        #         else:
        #             error = '请检查输入'
        #     else:
        #         form = forms.ResetpsdForm()
        #     return render(request, 'RBAC/resetpsd.html', {'form': form, 'error': error, 'title': '重置'})


@login_required
def logout_site(request):
    logout(request)
    return HttpResponseRedirect(reverse("articles:index"))


def global_settings(request):
    return {'ROOT_CONTEXT': settings.ROOT_CONTEXT}


@login_required
@csrf_exempt
def update_user_info(request):
    """
    用户信息修改
    """
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        sex = request.POST.get('sex')

        city = request.POST.get('city')
        desc = request.POST.get('sign')
        try:
            Profile.objects.update_or_create(user_id=user.id, defaults={'city': city, 'description': desc,
                                                                        "username": username, "sex": sex
                                                                        })
            return HttpResponse('{"status":"success"}', content_type='application/json')
        except Exception as e:
            logger.critical(e)
            return HttpResponse('{"status":"fail"}', content_type='application/json')


def user_home(request, user_id):
    """
    用户主页
    """
    try:
        user = User.objects.get(id=user_id)
    except Exception as e:
        logger.critical(e)
    # assets = Asset.objects.filter(asset_manager_id=user_id)
    # tasks = Task.objects.filter(task_user_id=user_id)
    return render(request, 'users/home.html', locals())


@login_required
def user_center(request):
    """
    用户中心
    """
    user = request.user
    scriptures = []
    musics = []
    collections = ArticleUser.objects.filter(Q(user=user) & Q(collect=1))

    for c in collections:
        article = c.article
        article.collection_time = c.c_time
        if article.category == 'scripture':
            scriptures.append(article)
        else:
            musics.append(article)

    return render(request, 'users/center.html', locals())


@login_required
def user_set(request):
    """
    用户配置
    """
    return render(request, 'users/set.html')


@login_required
@csrf_protect
def user_request_cancle(request):
    user = request.user
    error = ''
    if user.is_superuser:
        regist_id_list = request.POST.get('regist_id_list')
        regist_id_list = json.loads(regist_id_list)
        action = request.POST.get('action')
        for regist_id in regist_id_list:
            userregist = get_object_or_404(models.UserRequest, id=regist_id)
            userregist.status = '2'
            userregist.is_check = True
            userregist.is_use = True
            userregist.save()
        error = '已禁用'
    else:
        error = '权限错误'
    return JsonResponse({'error': error})


@login_required
@csrf_protect
def user_disactivate(request):
    user = request.user
    error = ''
    if user.is_superuser:
        user_list = request.POST.get('user_list')
        user_list = json.loads(user_list)
        action = request.POST.get('action')
        for user_mail in user_list:
            user_get = get_object_or_404(User, email=user_mail)
            if action == 'stop':
                user_get.is_check = True
                user_get.is_active = False
            elif action == 'start':
                user_get.is_active = True
            user_get.save()
        error = '已禁用'
    else:
        error = '权限错误'
    return JsonResponse({'error': error})


@csrf_exempt
@login_required
def upload_image(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        user = request.user
        try:
            Profile.objects.update_or_create(user=user, defaults={'avatar': avatar})
            data = {'state': 1}
        except Exception as e:
            logger.critical(e)
            data = {'state': 0}

        return JsonResponse(data)


def create_wechat_ticket(scene_str):
    url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={}".format(self.getAccessToken())
    data = {
        "expire_seconds": 300,
        "action_name": "QR_STR_SCENE",
        "action_info": {
            "scene": {
                "scene_str": scene_str
            }
        }
    }
    ret = s.post(url=url, data=json.dumps(data))
    return json.loads(ret.content)


def wechat_login(request):
    import uuid
    uid = uuid.uuid1()
    ticket = create_wechat_ticket("login_{}".format(uid))["ticket"]
    qrc = wpManager.getQrCode(ticket)
    return render(request, 'users/login.html', locals())