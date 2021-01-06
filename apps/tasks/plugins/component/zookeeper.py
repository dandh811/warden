from apps.assets.models import Port, Risk
import socket
import subprocess
from lib.wechat_notice import wechat
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'zookeeper'


def start(**kwargs):
    ports = Port.objects.filter(service_name__icontains=plugin)
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    for port in ports:
        ip = port.asset.ip

        logger.info('-' * 75)
        logger.info('%-30s%-30s' % ('+ Scan Target:', ip + '\t' + str(port.port_num)))  # 必须转换端口类型
        logger.info('%-30s%-30s' % ('- Scan Plugin:', '<zookeeper>'))

        try:
            socket.setdefaulttimeout(10)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port.port_num))
            s.send("success".encode('utf-8'))
            result = s.recv(1024).decode('utf-8')
            if "Environment" in result:
                desc = 'zookeeper 弱口令'
                Risk.objects.update_or_create(port=port, defaults={'asset': port.asset,
                                                                   'risk_type': 'weak_password',
                                                                   'desc': desc
                                                                   })
                logger.info('%-30s%-30s' % ('- Has Risk:', "[True], this host is vulnerable"))

        except Exception as e:
            logger.info('* %s' % e)

    logger.info('-' * 75)
