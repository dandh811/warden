from apps.assets.models import Risk
import requests
import urllib3
from lib.wechat_notice import wechat
from lib.common import update_scan_status
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

urllib3.disable_warnings()

plugin = 'cors'


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    if policy == 'increase':
        webapps = webapps.exclude(scanned__icontains='cors').order_by('-id')
    if not webapps:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))

    try:
        pool = ThreadPool(15)
        pool.map(check, webapps)
        pool.close()
        pool.join()
    except Exception as e:
        logger.critical(e)


def check(webapp):
    subdomain = webapp.subdomain
    logger.debug("[%s] [%s] %s" % (plugin, webapp.id, subdomain))

    origin = 'dandh811'
    headers = {
        'Origin': origin,
        'Cache-Control': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    try:
        r = requests.get(subdomain, timeout=5, headers=headers, allow_redirects=False, verify=False)
        resp_headers = dict((k.lower(), v) for k, v in r.headers.items())

        if resp_headers.get("access-control-allow-origin") == origin:
            if resp_headers.get("access-control-allow-credentials") == "true":
                logger.info('[$$$] 存在CORS跨域漏洞，允许发送身份信息')
                title = '发现CORS跨域漏洞漏洞'
                content = '-'
                wechat.send_msg(title, content)
                Risk.objects.update_or_create(target=subdomain, risk_type=plugin, defaults={'desc': resp_headers})
            else:
                logger.info('可能存在CORS跨域漏洞，但不允许发送身份信息')

    except Exception as e:
        logger.error(e)

    update_scan_status(webapp, plugin)
