import requests
from apps.assets.models import Port, Risk
from lib.wechat_notice import wechat
from loguru import logger
from lib.common import update_scan_status

timeout = 2
plugin = 'elasticsearch'


def start(**kwargs):
    policy = kwargs['policy']
    if policy == 'full':
        ports = Port.objects.filter(port_num='9200')
    else:
        ports = Port.objects.exclude(scanned__icontains=plugin).filter(port_num=9200)
    if not ports:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))

    protocols = ['http', 'https']
    for port in ports:
        ip = port.asset.ip
        for protocol in protocols:
            try:
                url = protocol + "://" + ip + ":" + str(port.port_num) + "/_cat"

                logger.debug("[%s] [%s] %s" % (plugin, port.id, url))
                response = requests.get(url)
                if "/_cat/master" in response.text:
                    logger.info('[$$$]success, 可以匿名访问')
                    Risk.objects.update_or_create(target=url, risk_type='elasticsearch匿名访问',
                                              defaults={'desc': 'elasticsearch匿名访问, ' + url})
                    logger.info("[True], this host is vulnerable")
                    title = 'elasticsearch匿名访问'
                    content = url
                    wechat.send_msg(title, content)
            except:
                pass
        update_scan_status(port, plugin)