"""
清理无效的服务器和web
"""
import requests
from django.conf import settings
import urllib3
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool
from apps.webapps.models import WebApp

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

plugin = 'sweep'


def start(**kwargs):
    webapps = kwargs['webapps']
    assets = kwargs['assets']
    try:
        pool = ThreadPool(30)
        pool.map(web_sweep, webapps)
        pool.close()
        pool.join()
    except Exception as e:
        logger.critical(e)

    try:
        pool = ThreadPool(30)
        pool.map(asset_sweep, assets)
        pool.close()
        pool.join()
    except Exception as e:
        logger.critical(e)


def web_sweep(webapp):
    url = webapp.subdomain

    try:
        res = requests.get(url, headers=settings.HTTP_HEADERS, timeout=30, verify=False, allow_redirects=False)
        if res.text:
            status_code = res.status_code
            # logger.info('+ 返回：' + str(status_code))
            if status_code not in settings.WORTHY_HTTP_CODE:
                # logger.info('* 返回：%s, 忽略' % status_code)
                if webapp.status == 'indeterminate':
                    webapp.delete()
                    logger.info('[%s] subdomain: %s, returned %s, deleted' % (plugin, url, status_code))
                else:
                    webapp.status = 'indeterminate'
                    logger.info('[%s] subdomain: %s, online --> indeterminate' % (plugin, url))
                    webapp.save()
            else:
                webapp.status_code = status_code
                if webapp.status == 'indeterminate':
                    webapp.status = 'online'
                    logger.info('[%s] subdomain: %s, indeterminate --> online' % (plugin, url))

                webapp.save()

        else:
            if webapp.status == 'indeterminate':
                webapp.delete()
                logger.info('[%s] subdomain: %s, content is null, deleted' % (plugin, url))
            else:
                webapp.status = 'indeterminate'
                webapp.save()
    except Exception as e:
        if webapp.status == 'indeterminate':
            webapp.delete()
            logger.info('[%s] subdomain: %s, returned error, deleted' % (plugin, url))
        else:
            webapp.status = 'indeterminate'
            logger.info('[%s] subdomain: %s, online --> indeterminate' % (plugin, url))

            webapp.save()


def asset_sweep(asset):
    try:
        ip = asset.ip
        res = WebApp.objects.filter(ip=ip)
        if not res:
            asset.delete()
            logger.info('%s Deleted' % ip)
    except Exception as e:
        logger.critical(e)
