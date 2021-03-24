from loguru import logger
import os.path
import subprocess
from django.conf import settings

plugin = 'wordpress'


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    if policy == 'increase':
        webapps = webapps.filter(other_info__icontains=plugin).exclude(scanned__icontains=plugin)
    else:
        webapps = webapps.filter(other_info__icontains=plugin)
    if not webapps:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    for webapp in webapps:
        url = webapp.subdomain
        logger.info('-' * 75)
        logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))
        try:
            report_path = '/opt/warden/warden/reports/wpscan/' + url.split('//')[1]
            if os.path.exists(report_path):
                continue
            else:
                cmd = 'wpscan --disable-tls-checks --api-token %s --url %s -o %s' % (settings.WPSCAN_API_TOKEN[0], url, report_path)
                subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        except Exception as e:
            logger.critical(e)