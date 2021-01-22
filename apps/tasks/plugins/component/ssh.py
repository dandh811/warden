from apps.assets.models import Risk, Port
from pexpect import pxssh
from django.conf import settings
from threading import *
maxConnections = 30
connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
from lib.wechat_notice import wechat
from lib.common import update_scan_status
from loguru import logger

plugin = 'ssh'


def start(**kwargs):
    policy = kwargs['policy']
    ports = Port.objects.filter(service_name__icontains=plugin)
    if policy == 'increase':
        ports = Port.objects.filter(service_name__icontains=plugin).exclude(scanned__contains=plugin)
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
        return
    usernames = settings.SSH_USERS

    with open('/opt/blog/blog/brute/passwords.txt', 'r') as f:
        passwords = f.readlines()

    for port in ports:
        ssh_brute(port, usernames, passwords)
        update_scan_status(port, plugin)


def connect(host, user, password, port, asset):
    global Found
    global Failes
    try:
        s = pxssh.pxssh()
        s.login(host, user, password, port.port_num)
        logger.info('Password Found:' + password)
        Found = True
        logger.info('发现弱口令：' + host + ' ' + str(port.port_num) + ' ' + user + ' ' + password)
        desc = user + ' : ' + password + ''
        Risk.objects.update_or_create(target=port.asset.ip, risk_type="ssh弱口令", defaults={
                'asset': asset, 'desc': desc})

    except Exception as e:
        pass
        # if 'read_nonblocking' in str(e): # 这个字符串表示主机连接次数过多,ssh不对外提供服务
        #     Failes += 1
        #     time.sleep(5)  # 休息5秒
        #     connect(host, user, password, False)  # 重新调用connect函数
    finally:
        connection_lock.release()


def ssh_brute(port, usernames, passwords):
    try:
        asset = port.asset
    except Exception as e:
        logger.critical(e)
        logger.info(port.id)
        port.delete()
        return

    ip = asset.ip
    logger.debug("[%s] [%s] %s" % (plugin, asset.id, ip))

    for username in usernames:
        for password in passwords:
            password = password.strip()
            if Found:
                return
            connection_lock.acquire()  # 锁定
            password = password.strip('\r\n')
            t = Thread(target=connect, args=(ip, username, password, port, asset))
            t.start()
