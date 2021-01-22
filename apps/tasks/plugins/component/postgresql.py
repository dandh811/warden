import psycopg2
from apps.assets.models import Port, Risk
from lib.wechat_notice import wechat
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

timeout = 2
plugin = 'postgresql'


def start(**kwargs):
    policy = kwargs['policy']
    if policy == 'full':
        ports = Port.objects.filter(service_name__icontains=plugin)
    else:
        ports = Port.objects.exclude(scanned__icontains=plugin).filter(service_name__icontains=plugin)
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
        return

    with open('/opt/blog/blog/brute/usernames.txt', 'r') as f:
        usernames = f.readlines()
    with open('/opt/blog/blog/brute/passwords.txt', 'r') as f:
        passwords = f.readlines()

    for port in ports:
        ip = port.asset.ip

        logger.info('-' * 75)
        logger.info('%-30s%-30s' % ('+ Scan Target:', ip + '\t' + str(port.port_num)))  # 必须转换端口类型
        logger.info('%-30s%-30s' % ('- Scan Plugin:', '< postgresql >'))

        for password in passwords:
            password = password.strip()
            for username in usernames:
                try:
                    username = username.strip()
                    psycopg2.connect(database="", user=username, password=password, host=ip, port=port.port_num)

                    desc = 'postgresql弱口令：%s:%s' % (username, password)
                    Risk.objects.update_or_create(port=port, defaults={'asset': port.asset,
                                                               'risk_type': 'postgresql弱口令',
                                                               'desc': desc
                                                               })

                    logger.info('[$$$]success')
                except Exception as e:
                    pass

    logger.info('-'*75)
