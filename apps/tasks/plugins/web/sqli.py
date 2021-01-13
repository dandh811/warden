from apps.assets.models import Risk
from lib.wechat_notice import wechat
import requests
import json
from apps.webapps.models import WebUrls
from lib.common import update_scan_status
import time
from loguru import logger

plugin = 'sqli'


def start(**kwargs):
    policy = kwargs['policy']
    if policy == 'full':
        weburls = WebUrls.objects.filter(url__contains='?').order_by('-id')
    else:
        weburls = WebUrls.objects.filter(url__contains='?').exclude(scanned__icontains='sqli').order_by('-id')

    if not weburls:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
        return
    denominator = len(weburls)
    molecular = 0
    for weburl in weburls:
        molecular += 1
        url = weburl.url
        logger.info('-' * 75)
        logger.debug("[%s] [%s] %s" % (plugin, weburl.id, url))
        data = sqlmap(url)
        try:
            if data:
                logger.info(data)
                logger.info('+ success, 发现SQL注入漏洞')
                Risk.objects.update_or_create(target=url, risk_type='SQL注入', defaults={'desc': data})

                title = '发现SQL注入漏洞'
                content = ''
                wechat.send_msg(title, content)
            else:
                logger.info('+ 未发现漏洞')
            update_scan_status(weburl, 'sqli')
        except Exception as e:
            logger.info('* %s' % e)

        if molecular == denominator:
            percent = 100.0
            logger.info('+ 进度: %s [%d/%d]' % (str(percent)+'%', molecular, denominator))
        else:
            percent = round(1.0 * molecular / denominator * 100, 2)
            logger.info('+ 进度 : %s [%d/%d]' % (str(percent)+'%', molecular, denominator))


def sqlmap(host):
    urlnew = "http://127.0.0.1:8775/task/new"
    urlscan = "http://127.0.0.1:8775/scan/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"
    }
    pd = requests.get(url=urlnew, headers=headers)
    jsons = pd.json()
    id = jsons['taskid']
    scan = urlscan + id + "/start"
    data = json.dumps({"url": "{}".format(host)})
    headers = {"Content-Type": "application/json"}
    requests.post(url=scan, headers=headers, data=data)
    status = "http://127.0.0.1:8775/scan/{}/status".format(id)
    n = 0
    while n < 60:
        staw = requests.get(url=status, headers=headers)
        if staw.json()['status'] == 'terminated':
            datas = requests.get(url='http://127.0.0.1:8775/scan/{}/data'.format(id))
            data = datas.json()['data']
            return data
        elif staw.json()['status'] == 'running':
            time.sleep(10)
        n += 1
