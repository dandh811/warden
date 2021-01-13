from apps.assets.models import Risk
from lib.wechat_notice import wechat
from loguru import logger
import subprocess
from lib.common import update_scan_status

plugin = 'php'


def start(**kwargs):
    policy = kwargs['policy']
    webapps = kwargs['webapps']

    if policy == 'increase':
        webapps = webapps.filter(other_info__icontains='php/').exclude(scanned__icontains=plugin)
    else:
        webapps = webapps.filter(other_info__icontains='php/')

    if not webapps:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    for webapp in webapps:
        url = webapp.subdomain

        logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))
        cmd = '/root/go/bin/phuip-fpizdam %s/index.php' % url
        logger.info(cmd)
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf-8')
        logger.info(out)
        logger.error(err.decode('utf-8'))
        if 'success' in out:
            Risk.objects.update_or_create(target=url, risk_type='php漏洞', defaults={'desc': cmd})

            logger.info('[$$$]success')
            title = '发现漏洞'
            content = plugin
            wechat.send_msg(title, content)
        update_scan_status(webapp, plugin)
        logger.info('-' * 75)
