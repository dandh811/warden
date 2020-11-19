from apps.cases.models import *
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def tools_index(request):
    return render(request, 'tools/tools_index.html', locals())


def tools_category(request, category):
    return render(request, 'tools/%s.html' % category, locals())


@csrf_exempt
def unicode2zh_p(request):
    content = request.POST.get('content')
    msg = content.encode('utf-8').decode('unicode_escape')
    return HttpResponse('{"status": "success", "msg": "%s"}' % msg, content_type='application/json')
