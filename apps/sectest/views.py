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