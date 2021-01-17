from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.sectest.models import *
from django.http import HttpResponse


@login_required
@csrf_exempt
def exploit_list(request):
    exps = Exploit.objects.order_by('-id')

    return render(request, 'exploit/exploit_list.html', locals())


def url_illegal_redirect(request, paras):
    """ URL 非法重定向漏洞 """
    source_host = request.META['REMOTE_ADDR']
    path = request.path
    full_path = request.get_full_path()

    Exploit.objects.update_or_create(source_host=source_host, type='url_illegal_redirect', path=path, full_path=full_path)

    return HttpResponse('{"status":"ok"}', content_type='application/json')


def postmessage(request):
    return render(request, 'sectest/attack.html')


def postmessage_child(request):
    return render(request, 'sectest/child.html')


def xss(request):
    return render(request, 'sectest/xss.html')


def xss_js(request):
    return render(request, 'sectest/xss.js')


@csrf_exempt
def xss_prey(requests):
    if 'HTTP_X_FORWARDED_FOR' in requests.META:
        ip = requests.META['HTTP_X_FORWARDED_FOR']
    else:
        try:
            ip = requests.META['REMOTE_ADDR']
        except:
            ip = '0.0.0.0'
    ip = ip.replace("'","\'")
    domain = requests.GET.get('domain','Unknown').replace("'","\'")
    user_agent = requests.META.get('HTTP_USER_AGENT','Unknown').replace("'","\'")
    # method = requests.method.replace("'","\'")
    cookie = requests.GET.get('data', 'No data').replace("'","\'")

    XssPrey.objects.create(domain=domain, user_agent=user_agent, cookie=cookie)
    # keep_alive = requests.GET.get('keepsession','0').replace("'","\'")
    # list = [now_time,ip,origin,software,method,data,keep_alive]
    # put_mysql(list,url)

    return HttpResponse('{"status":"ok"}', content_type='application/json')