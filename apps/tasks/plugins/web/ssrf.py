from apps.assets.models import Risk
from lib.wechat_notice import wechat
import requests
from apps.webapps.models import WebUrls
from lib.common import update_scan_status
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'ssrf'


def start(**kwargs):
    policy = kwargs['policy']

    if policy == 'full':
        weburls = WebUrls.objects.filter(url__contains='?').order_by('-id')
    else:
        weburls = WebUrls.objects.filter(url__contains='?').exclude(scanned__icontains=plugin).order_by('-id')

    if not weburls:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
        return
    keywords = ['share', 'wap', 'url', 'link', 'src', 'source', 'target', 'u', '3g', 'display', 'sourceURl',
                'imageURL', 'domain']
    for weburl in weburls:
        for keyword in keywords:
            _keyword = '?' + keyword + '='
            if _keyword in weburl.url:
                url = weburl.url.split(_keyword)[0] + _keyword + 'http://127.0.0.1:22'
                logger.debug("[%s] [%s] %s" % (plugin, weburl.id, url))
                try:
                    res = requests.get(url, timeout=10, verify=False, allow_redirects=False).content.decode('utf-8')

                    if 'mismatch' in res:
                        logger.info(res)
                        logger.info('[$$$] success, 发现%s漏洞' % url)
                        Risk.objects.update_or_create(webapp=url, risk_type=plugin, defaults={'desc': url})

                        title = '发现%s漏洞' % plugin
                        content = ''
                        wechat.send_msg(title, content)
                    update_scan_status(weburl, plugin)
                except Exception as e:
                    logger.critical(e)
