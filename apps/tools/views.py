from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from urllib import parse
from random import choice
import string


def tools_index(request):
    return render(request, 'hexo/tools.html', locals())


def test_index(request):
    return render(request, 'tools/1.html', locals())


def tools_category(request, category):
    return render(request, 'tools/%s.html' % category, locals())


@csrf_exempt
def unicode2zh_p(request):
    content = request.POST.get('content')
    msg = content.encode('utf-8').decode('unicode_escape')
    return HttpResponse('{"status": "success", "msg": "%s"}' % msg, content_type='application/json')


@csrf_exempt
def unicode2zh_n(request):
    content = request.POST.get('content')
    msg = str(content.encode('unicode_escape')).strip("b").strip("'")
    # msg = json.dumps(content)
    return HttpResponse('{"status": "success", "msg": "%s"}' % msg, content_type='application/json')


@csrf_exempt
def xss_encoding(request):
    source_str = request.POST.get('source_str')
    url_encoding = parse.quote(source_str)
    html_encoding = parse.quote(source_str)
    msg = {"url_encoding": url_encoding, "html_encoding": html_encoding}
    return HttpResponse('{"status": "success", "msg": "%s"}' % msg, content_type='application/json')


@csrf_exempt
def gen_password(request):
    pass_list = []
    length = request.POST.get('source_str')
    for i in range(int(length)):
        pass_list.append(choice(string.ascii_letters+string.digits))
    msg = ''.join(pass_list)

    return HttpResponse('{"status": "success", "msg": "%s"}' % msg, content_type='application/json')