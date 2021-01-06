from apps.webapps.models import WebUrls
import simplejson
import subprocess
from lib.common import update_scan_status
from urllib import parse
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'crawlergo'


def get_urls(webapp):
    logger.debug("[%s] [%s] %s" % (plugin, webapp.id, webapp.subdomain))
    cmd = "/opt/tools/crawlergo -c /opt/tools/chrome-linux/chrome -o json " + webapp.subdomain
    try:
        rsp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = rsp.communicate()
        result = simplejson.loads(out.decode().split("--[Mission Complete]--")[1])
        if not result:
            return
        req_list = result["req_list"]
        params = []
        for req in req_list:
            url = req['url']
            if 'wp-json' in url:
                continue
            parseResult = parse.urlparse(url)
            param_dict = parse.parse_qs(parseResult.query)
            res = set(param_dict.keys()).difference(set(params))
            if res:
                logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))
                WebUrls.objects.update_or_create(url=url, webapp=webapp, scanned='not')

                for p in res:
                    if p not in params:
                        params.append(p)
    except Exception as e:
        logger.critical(e)
    finally:
        update_scan_status(webapp, 'crawlergo')


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']

    if policy == 'increase':
        webapps = webapps.exclude(scanned__icontains=plugin).order_by('-id')
    if not webapps:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
    else:
        try:
            pool = ThreadPool(10)
            pool.map(get_urls, webapps)
            pool.close()
            pool.join()
        except Exception as e:
            logger.critical(e)
