from apps.assets.models import Risk
import requests
import urllib3
from lib.wechat_notice import wechat
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

urllib3.disable_warnings()

plugin = 'jenkins'


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    assets = kwargs['assets']
    if not webapps:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    for webapp in webapps:
        if not webapp.other_info:
            continue
        if 'jenkins' in webapp.other_info:
            url = webapp.subdomain
            logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))

            payload = "/securityRealm/user/admin/descriptorByName/org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition/checkScriptCompile"

            try:
                r = requests.get(url + payload, timeout=5, verify=False)
                if 'java.lang.NullPointerException' in r.text:
                    Risk.objects.update_or_create(target=url, risk_type='jenkins漏洞', defaults={
                                                                       'desc': 'jenkins远程命令执行漏洞，编号：CVE-2018-1000861'
                                                                       })
                    logger.info(webapp.ip + ':' + ' 存在Jenkins漏洞')
            except Exception as e:
                logger.info('* %s' % e)
