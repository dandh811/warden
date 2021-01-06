from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.payloads.models import Payload


@login_required
@csrf_exempt
def payloads_list(request, page):
    if request.method == 'GET':
        objects_all = Payload.objects.all().order_by('-id')
        paginator = Paginator(objects_all, 30)
        try:
            objects = paginator.get_page(page)
        except PageNotAnInteger:
            objects = paginator.get_page(1)
        except EmptyPage:
            objects = paginator.get_page(paginator.num_pages)

    return render(request, 'payloads/payloads_list.html', locals())


# def url_illegal_redirect(request, paras):
#     """ URL 非法重定向漏洞 """
#     source_host = request.META['REMOTE_ADDR']
#     path = request.path
#     full_path = request.get_full_path()
#
#     Exploit.objects.update_or_create(source_host=source_host, type='url_illegal_redirect', path=path, full_path=full_path)
#
#     return HttpResponse('{"status":"ok"}', content_type='application/json')