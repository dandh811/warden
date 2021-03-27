from apps.webapps.models import WebUrls, WebApp
import subprocess
from lib.common import update_scan_status
from loguru import logger
import requests
from django.conf import settings

plugin = 'dirsearch'


def get_urls(webapp):
    logger.debug("[%s] [%s] %s" % (plugin, webapp.id, webapp.subdomain))
    cmd = "python3 /opt/tools/dirsearch/dirsearch.py -u %s --simple-report=/tmp/dirsearch.txt -w /opt/warden/warden/brute/Filenames_or_Directories_All.txt" % webapp.subdomain
    logger.debug(cmd)
    try:
        try:
            r = requests.get(webapp.subdomain, headers=settings.HTTP_HEADERS, timeout=10, verify=False,
                             allow_redirects=False)
            if r.status_code != 403:
                webapp.status_code = r.status_code
                webapp.save()
                logger.info(webapp.status_code)
                return

        except Exception as e:
            logger.error(e)
            return
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        logger.debug(out.decode())
        with open('/tmp/dirsearch.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                url = line.strip()
                try:
                    r = requests.get(url, headers=settings.HTTP_HEADERS, timeout=10, verify=False,
                                     allow_redirects=False)
                    if 'not found' in r.text:
                        break
                except Exception as e:
                    logger.error(e)
                    continue
                logger.info("[%s] %s" % (plugin, url))
                WebUrls.objects.update_or_create(url=url, webapp=webapp)
    except Exception as e:
        logger.critical(e)
    finally:
        update_scan_status(webapp, plugin)


def start(**kwargs):
    policy = kwargs['policy']

    if policy == 'increase':
        webapps = WebApp.objects.filter(status_code=403).exclude(scanned__icontains=plugin)
    else:
        webapps = WebApp.objects.filter(status_code=403)
    if not webapps:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))
    else:
        for webapp in webapps:
            get_urls(webapp)
