from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.financial2.models import *
from django.db.models import Q
from loguru import logger
import requests
import json


@csrf_exempt
def wxlogin(request):
    code = request.GET['code']
    nick = request.GET['nick']
    avaurl = request.GET['avaurl']
    city = request.GET['city']
    sex = request.GET['sex']
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=wx28ee3f389ffbf8b0&secret=8bffe9c08d8a478deb335fa3a9fa6443&js_code=' + code + '&grant_type=authorization_code'
    # Appid为开发者appid.appSecret为开发者的appsecret, 都可以从微信公众平台获取；
    res = requests.get(url)  # 发送HTTPs请求并获取返回的数据，推荐使用curl
    res = json.loads(res.text)
    logger.info(res)
    openid = res['openid']
    session_key = res['session_key']

    Investors.objects.update_or_create(openid=openid,
                                       defaults={"session_key": session_key, "nick": nick, "avaurl": avaurl,
                                                 "city": city, "sex": sex})


@csrf_exempt
def add_message(request):
    try:
        if request.method == 'POST':
            openid = request.POST.get('openid')
            platform = request.POST.get('platform')
            bank = request.POST.get('bank')
            rate = request.POST.get('rate')
            start = request.POST.get('start')
            end = request.POST.get('end')
            try:
                Article.objects.create(title=title, content=content, category='message')
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                logger.critical(e)
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            return render(request, 'article/add_message.html', locals())
    except Exception as e:
        logger.critical(e)