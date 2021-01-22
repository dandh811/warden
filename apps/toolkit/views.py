from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import xmltodict
import base64
from apps.toolkit.libs.whathash import check
import whois
import datetime
from urllib.parse import quote
from loguru import logger


def index(request):
    toolkits = [
        {"display": "XSS编码", "type": "penetration", "name": "xss"},
        {"display": "base64", "type": "development", "name": "base64"},

    ]
    return render(request, 'toolkit/index.html', locals())


@csrf_exempt
def json_xml(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        if type == 'json_to_xml':
            json_data = request.POST.get('json_data')
            if not json_data:
                res_data = {"msg": '-1'}
            elif '{' not in json_data:
                res_data = {"msg": '-2'}
            else:
                try:
                    _json_data = json.loads(json_data)
                    xml_data = xmltodict.unparse(_json_data)
                    res_data = {"msg": xml_data}
                except Exception as e:
                    res_data = {"msg": '-2'}

        else:
            xml_data = request.POST.get('xml_data')
            try:
                json_data = xmltodict.parse(xml_data)
            except Exception as e:
                json_data = e
            res_data = {"msg": json_data}

        msg = json.dumps(res_data)
        return HttpResponse(msg, content_type='application/json')
    else:
        return render(request, 'toolkit/json_xml.html', locals())


@csrf_exempt
def base64_handle(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        if type == 'base64_encode':
            left_data = request.POST.get('left_data').encode('utf-8')
            right_data = base64.b64encode(left_data).decode()
            res_data = {"msg": right_data}
        else:
            right_data = request.POST.get('right_data').encode('utf-8')
            left_data = base64.b64decode(right_data).decode()
            res_data = {"msg": left_data}

        msg = json.dumps(res_data)
        return HttpResponse(msg, content_type='application/json')
    else:
        return render(request, 'toolkit/base64.html', locals())


@csrf_exempt
def whathash(request):
    if request.method == 'POST':
        left_data = request.POST.get('left_data')
        res = check(left_data)
        res_data = {"msg": res}

        msg = json.dumps(res_data)
        return HttpResponse(msg, content_type='application/json')
    else:
        return render(request, 'toolkit/whathash.html', locals())


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


@csrf_exempt
def whois_handle(request):
    if request.method == 'POST':
        left_data = request.POST.get('left_data')
        res = whois.whois(left_data)
        res_data = {"msg": res}

        msg = json.dumps(res_data, cls=DateEncoder)
        return HttpResponse(msg, content_type='application/json')
    else:
        return render(request, 'toolkit/whois.html', locals())


@csrf_exempt
def xss(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data')
        url_data = quote(input_data)
        ascii_data = np.fromstring(input_data, dtype=np.uint8).tolist()
        ascii_data = ' '.join([str(i) for i in ascii_data])
        res_data = {"ascii_data": ascii_data, "url_data": url_data}

        msg = json.dumps(res_data)
        return HttpResponse(msg, content_type='application/json')
    else:
        return render(request, 'toolkit/xss.html', locals())


@csrf_exempt
def smuggler(request):
    if request.method == 'GET':
        referer = request.META.get('HTTP_REFERER')
        if referer:
            msg = '+ [success] ' + referer
        else:
            msg = '* referer 为空'
        logger.info(msg)
        return HttpResponse(msg, content_type='text')
    else:
        return render(request, 'toolkit/xss.html', locals())


@csrf_exempt
def find_subdomains(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data')
        domain = input_data.strip()
        subdomains = '\n'.join(get_target_subdomains_virustotal(domain))
        logger.info(subdomains)
        res_data = {"msg": subdomains}

        msg = json.dumps(res_data)
        return HttpResponse(msg, content_type='application/json')
    else:

        return render(request, 'toolkit/find_subdomains.html')
