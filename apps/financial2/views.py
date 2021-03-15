from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.financial2.models import *
from loguru import logger
import requests
import json
import datetime
import decimal
from django.db.models import Sum


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


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

    return HttpResponse('{"status":"success", "openid": "%s"}' % openid, content_type='application/json')


@csrf_exempt
def new(request):
    try:
        if request.method == 'POST':
            openid = request.POST.get('openid')
            platform = request.POST.get('platform')
            bankName = request.POST.get('bankName')
            capital = request.POST.get('capital')

            rate = request.POST.get('rate')
            start = request.POST.get('start')
            end = request.POST.get('end')
            start = datetime.datetime.strptime(start, '%Y-%m-%d')
            end = datetime.datetime.strptime(end, '%Y-%m-%d')
            platform = Platform.objects.get(name=platform)
            investors = Investors.objects.get(openid=openid)
            Bank.objects.update_or_create(name=bankName)
            bank = Bank.objects.get(name=bankName)
            try:
                Investment.objects.create(investors=investors, platform=platform, capital=int(capital), bank=bank,
                                          year_rate=float(rate), start_date=start, end_date=end)
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                logger.critical(e)
                return HttpResponse('{"status": 0}', content_type='application/json')
    except Exception as e:
        logger.critical(e)


@csrf_exempt
def get_investment(request):
    if request.method == 'POST':
        res = {}
        data = []
        openid = json.loads(request.body)['openid']

        investors = Investors.objects.get(openid=openid)
        try:
            investments = Investment.objects.filter(investors=investors).order_by('-id')
            for i in investments:
                item = {}
                item["platform"] = i.platform.name
                item["bank"] = i.bank.name
                item["capital"] = i.capital
                item["rate"] = i.year_rate
                item["start"] = str(i.start_date)
                item["end"] = str(i.end_date)
                item["interest_day"] = i.interest_day
                item["interest_total"] = i.interest_total
                data.append(item)
            res["data"] = data

            return HttpResponse(json.dumps(res, cls=DecimalEncoder))
        except Exception as e:
            logger.critical(e)
            return HttpResponse('{"status": 0}', content_type='application/json')


@csrf_exempt
def get_statistical(request):
    if request.method == 'POST':
        try:
            openid = json.loads(request.body)['openid']
            logger.info(openid)
            investors = Investors.objects.get(openid=openid)
            investments = Investment.objects.filter(investors=investors)
            capital = Investment.objects.filter(completed='no').aggregate(nums=Sum("capital"))

            get_interest = 0
            interest_day = 0
            res = {}
            for i in investments:
                if i.completed == 'yes':
                    # 如果该笔投资已经完成，所有总收益直接加入该笔投资的总收益，否则按投资天数计算；
                    # 如果该笔投资已经完成，每日收益忽略；
                    get_interest += i.interest_total
                else:
                    get_interest += i.interest_day * (datetime.date.today() - i.start_date).days
                    interest_day += i.interest_day
            res['total_principal'] = capital['nums']
            res['get_interest'] = get_interest
            res['interest_day'] = interest_day

            latest_inv = Investment.objects.filter(completed='no').earliest('end_date')
            latest_inv_info = '%s:%s:%d:%s' % (
            latest_inv.platform, latest_inv.bank, latest_inv.capital, latest_inv.end_date)
            res['latest_inv_info'] = latest_inv_info

            return HttpResponse(json.dumps(res, cls=DecimalEncoder))
        except Exception as e:
            logger.critical(e)
            return HttpResponse('{"status": 0}', content_type='application/json')
