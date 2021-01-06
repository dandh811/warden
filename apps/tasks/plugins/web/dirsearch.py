from apps.webapps.models import WebUrls
import simplejson
import subprocess
from lib.common import update_scan_status
from urllib import parse
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'dirsearch'


def get_urls(webapp):
    logger.debug("[%s] [%s] %s" % (plugin, webapp.id, webapp.subdomain))
    cmd = "python3 /opt/tools/dirsearch/dirsearch.py -u %s -e * --simple-report=/tmp/dirsearch.txt -x 403,404" % webapp.subdomain
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        logger.debug(out.decode())
        with open('/tmp/dirsearch.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                url = line.strip()
                logger.info("[%s] %s" % (plugin, url))
                WebUrls.objects.update_or_create(url=url, webapp=webapp, scanned='not')
    except Exception as e:
        logger.critical(e)
    # finally:
    #     update_scan_status(webapp, plugin)


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']

    if policy == 'increase':
        webapps = webapps.exclude(scanned__icontains=plugin)
    if not webapps:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
    else:
        for webapp in webapps:
            get_urls(webapp)
