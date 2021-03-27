from apps.assets.models import Port, Risk
import socket
from lib.wechat_notice import wechat
from loguru import logger

plugin = 'memcache'


def start(**kwargs):
    policy = kwargs['policy']
    assets = kwargs['assets']

    ports = Port.objects.filter(asset_id__in=assets, service_name__icontains='memcache')
    if not ports:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))

    for port in ports:
        ip = port.asset.ip

        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))

        try:
            socket.setdefaulttimeout(10)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port.port_num))
            s.send(b'\x73\x74\x61\x74\x73\x0a')
            result = s.recv(2048).decode('utf-8')
            if result and ('STAT version' in result):
                desc = ip + ' ' + str(port.port_num)
                Risk.objects.update_or_create(target=ip, risk_type='memcache空口令', defaults={'desc': desc})
                logger.info("[$$$]success")
        except Exception as e:
            pass
