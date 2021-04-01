import re
from celery import shared_task
from apps.tasks.models import Plugins
from apps.webapps.models import WebApp
from apps.assets.models import Asset
from django.db.models import Q
from apps.tasks import asset_discovery
import requests
import urllib3
from apps.tasks import subdomain_scan
from loguru import logger

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
from apps.tasks.plugins.component import docker, jenkins, memcache, mongodb, ssh, redis, \
    wordpress, zookeeper, ftp, mysql, nfs, elasticsearch, tomcat, postgresql, weblogic, \
    cve_2020_1938, zabbix, php, rsync, struts2
from apps.tasks.plugins.web import crlf, cors, aws_s3, xray, dirsearch, \
    subdomain_takeover,  \
    smuggling, crawlergo, sqli, ssrf, open_redirect, postmessage
from apps.tasks.plugins import awvs, sweep


def vul_scan(task):
    logo = """
                           _              
                          | |             
 __      __ __ _  _ __  __| |  ___  _ __  
 \ \ /\ / // _` || '__|/ _` | / _ \| '_ \ 
  \ V  V /| (_| || |  | (_| ||  __/| | | |
   \_/\_/  \__,_||_|   \__,_| \___||_| |_|
                                          
                                          """
    logger.info(logo)

    # start(task)
    start.delay(task)


@shared_task
def start(task):
    try:
        targets = task.target
        webapps, assets = get_specific_targets(targets)
        params = {"targets": targets, "webapps": webapps, "assets": assets, "policy": task.policy}

        plugins = task.plugins.all()
        logger.warning('Scan Policy: ' + task.policy)

        for plugin in plugins:
            if plugin.name == 'all':
                while True:
                    subdomain_scan.start(task)

                    plugins_ = Plugins.objects.exclude(name__in=['all', 'jenkins', 'sweep', 'smuggling', 'postmessage', 'dirsearch'])
                    for p in plugins_:
                        eval(p.name).start(**params)
            else:
                eval(plugin.name).start(**params)
    except Exception as e:
        logger.critical(e)

    logger.warning('Task done!')


def get_specific_targets(targets):
    targets = targets.strip().replace('，', ',').strip(',')
    if targets == '*':
        logger.warning('Scan Target: ALL')
        webapps = WebApp.objects.all()
        assets = Asset.objects.all()
    elif re.match(r'\d+.\d+.\d+.', targets):
        # 支持扫描各种IP组合形式
        logger.warning('scan target: ' + targets)
        ips = asset_discovery.add_nmap_scan(targets)
        webapps = []
        assets = []
        for ip in ips:
            asset = Asset.objects.filter(ip=ip)[0]
            assets.append(asset)
    else:
        logger.warning('Scan Target: ' + targets)
        assets = []
        targets = targets.split(',')
        targets = list(map(lambda x: x.strip(), targets))
        webapps = WebApp.objects.filter(Q(domain__in=targets) | Q(subdomain__in=targets)).filter(in_scope='yes')
        for webapp in webapps:
            if not webapp.ip:
                continue
            asset = Asset.objects.filter(ip=webapp.ip)
            if asset and asset not in assets:
                assets.append(asset[0])
    return webapps, assets
