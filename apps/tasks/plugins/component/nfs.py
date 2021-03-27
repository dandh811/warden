from apps.assets.models import Port, Risk
import socket
import os
from lib.wechat_notice import wechat
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

timeout = 2

plugin = 'nfs'


def start(**kwargs):
    policy = kwargs['policy']
    if policy == 'full':
        ports = Port.objects.filter(service_name__icontains=plugin)
    else:
        ports = Port.objects.exclude(scanned__icontains=plugin).filter(service_name__icontains=plugin)
    if not ports:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))
        return

    for port in ports:
        ip = port.asset.ip

        logger.info('-' * 75)
        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))

        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address = (ip, int(port.port_num))
            status = cs.connect_ex((address))
            # 若返回的结果为0表示端口开启
            cmd = ["showmount", "-e", ip]
            output = os.popen(" ".join(cmd)).read()
            if 'Export list' in output:
                logger.info('[$$$]success')
                Risk.objects.update_or_create(target=ip, defaults={'asset': port.asset,
                                                               'risk_type': 'nfs未授权访问',
                                                               'desc': output})
            cs.close()

        except Exception as e:
            logger.info(e)
            continue
