from apps.cases.models import *
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import mistune
from loguru import logger


def cases_index(request):
    fps_all = FunctionPoint.objects.all()
    paginator = Paginator(fps_all, 10)
    page = request.GET.get('page')
    fps = paginator.get_page(page)
    fields = CaseField.objects.all()
    vuls = Vul.objects.all()
    for f in fps:
        f.f_vuls = f.vuls.all()

    return render(request, 'cases/cases_index.html', locals())


@csrf_exempt
def cases_search(request):
    fields = CaseField.objects.all()
    vuls = Vul.objects.all()

    field = request.POST.get('field')
    vul = request.POST.get('vul')
    q = request.POST.get('cases_search')

    if field:
        cases_filter = Case.objects.filter(case_field__name=field)
    else:
        cases_filter = Case.objects.all()
    if vul:
        cases_filter = cases_filter.filter(vul__name=vul)
    if q:
        cases_filter = cases_filter.filter(Q(name__icontains=q) | Q(content__icontains=q) | Q(vul__name=q))

    paginator = Paginator(cases_filter, 10)
    page = request.GET.get('page')
    cases = paginator.get_page(page)

    return render(request, 'cases/cases_index.html', locals())


@csrf_exempt
def case_detail(request, field, vul, function):
    try:
        case_general = Case.objects.get(Q(case_field__name=field) & Q(type='general') & Q(vul__name=vul))
        mk = mistune.Markdown()
        output_general = mk(case_general.content)
    except Exception as e:
        logger.critical(e)

    try:
        case_special = Case.objects.get(Q(case_field__name=field) & Q(type='special') & Q(vul__name=vul) & Q(function_point__name=function))
        mk = mistune.Markdown()
        output_special = mk(case_special.content)
    except Exception as e:
        logger.critical(e)

    return render(request, 'cases/case.html', locals())
