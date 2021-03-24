from apps.assets.models import Port, Risk
from django.conf import settings
from threading import *
from lib.wechat_notice import wechat
from loguru import logger
import socket
from lib.common import update_scan_status
import pymysql

maxConnections = 30
connection_lock = BoundedSemaphore(value=maxConnections)

plugin = 'mysql'
timeout = 2


def start(**kwargs):
    policy = kwargs['policy']
    if policy == 'full':
        ports = Port.objects.filter(service_name__icontains=plugin)
    else:
        ports = Port.objects.exclude(scanned__icontains=plugin).filter(service_name__icontains=plugin)
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    usernames = settings.MYSQL_USERS

    with open('/opt/warden/warden/brute/passwords.txt', 'r') as f:
        passwords = f.readlines()

    for port in ports:
        ip = port.asset.ip
        logger.info('-' * 75)
        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(3)
        try:
            sk.connect((ip, port.port_num))
        except:
            port.delete()
            logger.info('port deleted')
            continue
        for password in passwords:
            password = password.strip()
            for username in usernames:
                try:
                    t = Thread(target=mysql_brute, args=(ip, port, username, password))
                    t.start()
                except Exception as e:
                    logger.info(e)
                    continue
        update_scan_status(port, plugin)


def mysql_brute(ip, port, user, passwd):
    try:
        pymysql.Connect(
            host=ip,
            port=port.port_num,
            user=user,
            passwd=passwd,
            connect_timeout=1
        )

        logger.info('+ mysql login successful!')
        logger.info('+ %s:%s' % (user, passwd))
        Risk.objects.update_or_create(port=port, defaults={'asset': port.asset,
                                                           'risk_type': 'mysql弱口令',
                                                           'desc': '%s:%s' % (user, passwd)
                                                           })

        logger.info("[$$$]success, ")

    except Exception as e:
        pass
