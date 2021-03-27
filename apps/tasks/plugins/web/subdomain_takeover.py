import subprocess
import re
from urllib.parse import urlparse
from apps.assets.models import Risk
from lib.common import update_scan_status
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'subdomain_takeover'

payloads = ['airee.ru', 'Bitbucket', 'Campaign Monitor', 'Cargo Collective',
            'Digital Ocean', 'Fastly', 'Feedpress', 'Fly.io',
            'Ghost', 'github', 'HatenaBlog', 'Juice', 'Help Scout', 'Heroku', 'Intercom', 'JetBrains', 'Kinsta',
            'LaunchRock', 'Mashery', 'azure', 'Netlify', 'Pantheon', 'Readme.io', 'Statuspage',
            'Strikingly', 'Surge.sh', 'Tumblr', 'Tilda', 'Uptimerobot', 'UserVoice', 'Webflow', 'Wordpress',
            'zendesk', 'hubspot', 'uptimerobot', 'atlassian',
            'fly.io', 'tilda.cc', 'azure',]


def start(**kwargs):
    webapps = kwargs['webapps'].filter(status_code__in=[404, 500])

    if not webapps:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))

    try:
        pool = ThreadPool(50)
        pool.map(check, webapps)
        pool.close()
        pool.join()
    except Exception as e:
        logger.critical(e)


def check(webapp):
    subdomain = webapp.subdomain
    logger.debug("[%s] [%s] %s" % (plugin, webapp.id, subdomain))

    netloc = urlparse(subdomain).netloc.split(':')[0]
    if not bool(re.search('[a-z]', netloc)):  # 判断url是域名还是IP
        return

    try:
        cmd = 'host ' + netloc
        res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = res.communicate()
        out = out.decode('utf-8')
        if 'alias' not in out:
            return
        if 'elb.amazonaws.com' in out:
            return

        for payload in payloads:
            payload = payload.lower()
            if payload in out:
                Risk.objects.update_or_create(target=subdomain, risk_type='子域名劫持', defaults={'desc': payload})
                logger.info('[$$$] 发现漏洞：%s, %s' % (subdomain, payload))
        update_scan_status(webapp, 'subdomain_takeover')

    except Exception as e:
        logger.critical(e)
