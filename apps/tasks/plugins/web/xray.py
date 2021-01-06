from apps.webapps.models import WebUrls, WebApp
from lib.common import update_scan_status
import time
from loguru import logger
import subprocess

plugin = 'xray'


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    xray_plugins = 'xss, cmd_injection, crlf_injection, jsonp, path_traversal, redirect, sqldet, ssrf, phantasm'
    if policy == 'full':
        weburls = WebUrls.objects.filter(url__contains='?')
        webapps = webapps.exclude(status_code=404)
    else:
        weburls = WebUrls.objects.filter(url__contains='?').exclude(scanned__icontains=plugin)
        webapps = WebApp.objects.exclude(scanned__icontains=plugin).exclude(status_code=404)
    if not weburls:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
        return
    logger.info('有效url数： %s' % len(weburls))
    for weburl in []:
        url = weburl.url
        logger.debug("[%s] [%s] %s" % (plugin, weburl.id, url))

        try:
            command = '/opt/tools/xray webscan --url %s --html-output /opt/blog/blog/reports/xray/%s.html' % (url, url.split('//')[1])
            p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

            while True:
                status = subprocess.Popen.poll(p)
                time.sleep(5)
                if status or status == 0:
                    break
            update_scan_status(weburl, plugin)
        except Exception as e:
            logger.critical(e)

    for webapp in webapps:
        url = webapp.subdomain
        logger.info('-' * 75)
        logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))

        try:
            command = '/opt/tools/xray webscan --basic-crawler %s --html-output /opt/blog/blog/reports/xray/%s.html' % (url, url.split('//')[1])
            c = subprocess.call(command, shell=True)
            # out, err = res.communicate()
            # out = out.decode('utf-8')
            # if data:
            #     logger.info(data)
            #     logger.info('+ success, 发现%s漏洞' % plugin_name)
            #     Risk.objects.update_or_create(webapp=url, risk_type=plugin_name, defaults={'desc': data})
            #
            #     title = '发现%s漏洞' % plugin_name
            #     content = ''
            #     wechat.send_msg(title, content)
            # else:
            #     logger.info('+ 未发现漏洞')
            update_scan_status(webapp, plugin)
        except Exception as e:
            logger.critical(e)
