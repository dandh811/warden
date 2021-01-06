import ftplib
from apps.assets.models import Port, Risk
from lib.wechat_notice import wechat
from loguru import logger
from lib.common import update_scan_status

timeout = 2

plugin = 'ftp'


def start(**kwargs):
    policy = kwargs['policy']
    if policy == 'full':
        ports = Port.objects.filter(service_name__icontains=plugin)
    else:
        ports = Port.objects.exclude(scanned__icontains=plugin).filter(service_name__icontains=plugin)
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    with open('/opt/warden/warden/brute/usernames.txt', 'r') as f:
        usernames = f.readlines()
    with open('/opt/warden/warden/brute/passwords.txt', 'r') as f:
        passwords = f.readlines()

    ftp = ftplib.FTP()
    for port in ports:
        ip = port.asset.ip

        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))

        try:
            ftp.connect(ip, port.port_num, timeout=5)
            logger.info('ftp connected')
        except Exception as e:
            logger.error(e)
            port.delete()
            logger.info('port deleted')
            continue
        try:
            ftp.login('', '')
            logger.info('ftp login successful!')
            Risk.objects.update_or_create(target=ip, risk_type='ftp匿名登录', defaults={'target': ip, 'desc': 'ftp匿名登录'})
            logger.info("[True], this host is vulnerable")
            continue
        except Exception as e:
            logger.error(e)

        for username in usernames:
            username = username.strip()
            for password in passwords:
                password = password.strip()
                try:
                    # logger.debug(username + ':' + password)
                    ftp.login(username, password)

                    logger.info('FTP login successful!')
                    logger.info('[$$$] %s:%s' % (username, password))
                    Risk.objects.update_or_create(target=ip, risk_type='ftp弱口令', defaults={
                                                                       'desc': '%s:%s' % (username, password)
                                                                       })

                    title = 'ftp弱口令'
                    content = ''
                    wechat.send_msg(title, content)
                except Exception as e:
                    # logger.info(e)
                    pass
        update_scan_status(port, plugin)

        logger.info('-'*75)
