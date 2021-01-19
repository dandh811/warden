from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.sectest.models import *
from django.http import HttpResponse
from lib.wechat_notice import wechat
from loguru import logger


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

    try:
        XssPrey.objects.update_or_create(domain=domain, user_agent=user_agent, cookie=cookie, ip=ip)

        title = '发现XSS猎物'
        content = domain

        wechat.send_msg(title, content)
    except Exception as e:
        logger.critical(e)

    return HttpResponse('{"status":"ok"}', content_type='application/json')