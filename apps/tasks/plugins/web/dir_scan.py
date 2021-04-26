from apps.assets.models import Risk
from lib.wechat_notice import wechat
import requests
from apps.webapps.models import WebApp
from lib.common import update_scan_status
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'dir_scan'


def start(**kwargs):
    policy = kwargs['policy']

    if policy == 'full':
        webapps = WebApp.objects.all()
    else:
        webapps = WebApp.objects.filter(status_code=404).exclude(scanned__icontains=plugin)

    if not webapps:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))
        return
    keywords = ['admin']
    for webapp in webapps:
        for keyword in keywords:
            url = webapp.subdomain + '/' + keyword
            try:
                res = requests.get(url, timeout=10, verify=False, allow_redirects=False).content.decode('utf-8')

                if res:
                    logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))

                    if 'not found' in res:
                        continue
                    if 'doesn’t exist' in res:
                        continue
                    if 'nginx' in res:
                        continue
                    if 'Cannot GET /admin' in res:
                        continue
                    if 'Access Denied' in res:
                        continue
                    logger.info(res)
                    # logger.info('[$$$] success, 发现%s漏洞' % url)
                    # Risk.objects.update_or_create(target=url, risk_type=plugin, defaults={'desc': url})
                    # title = '发现%s漏洞' % plugin
                    # content = '-'
                    # wechat.send_msg(title, content)
                # update_scan_status(weburl, plugin)
            except Exception as e:
                pass
