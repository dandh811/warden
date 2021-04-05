from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from apps.sectest.models import *
from django.http import HttpResponse
from lib.wechat_notice import wechat
from loguru import logger
import json
from urllib.parse import unquote


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


def pypi_test_download(request):
    return render(request, 'sectest/pypi_test.txt')


def pypi_test_upload(request):
    if request.method == 'POST':
        try:
            msg = json.loads(request.body)
            logger.info(msg)
            PackagePrey.objects.update_or_create(msg=msg)
        except Exception as e:
            logger.critical(e)

        return HttpResponse('{"status":"ok"}', content_type='application/json')


@csrf_exempt
def xss_prey(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        try:
            ip = request.META['REMOTE_ADDR']
        except:
            ip = '0.0.0.0'

    ip = ip.replace("'","\'")
    domain = request.GET.get('domain','Unknown').replace("'","\'")
    user_agent = request.META.get('HTTP_USER_AGENT','Unknown').replace("'","\'")
    # method = requests.method.replace("'","\'")
    full_path = request.get_full_path()
    full_path = unquote(full_path)

    logger.debug(full_path)
    cookie = full_path
    logger.info(cookie)
    try:
        XssPrey.objects.update_or_create(domain=domain, user_agent=user_agent, cookie=cookie, ip=ip)

        title = '发现XSS猎物'
        content = domain

        wechat.send_msg(title, content)
    except Exception as e:
        logger.critical(e)

    return HttpResponse('{"status":"ok"}', content_type='application/json')