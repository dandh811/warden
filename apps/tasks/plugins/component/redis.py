from apps.assets.models import Port, Risk
import socket
import subprocess
from lib.wechat_notice import wechat
from loguru import logger
from django.db.models import Q

plugin = 'redis'


def start(**kwargs):
    policy = kwargs['policy']
    assets = kwargs['assets']
    if policy == '*':
        ports = Port.objects.filter(Q(service_name__icontains='redis') | Q(port_num=6379))
    else:
        ports = Port.objects.filter(Q(service_name__icontains='redis') | Q(port_num=6379)).exclude(scanned__contains=plugin)

    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
    with open('/opt/blog/blog/brute/passwords.txt', 'r') as f:
        passwords = f.readlines()
    for port in ports:
        ip = port.asset.ip
        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))
        try:
            socket.setdefaulttimeout(10)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port.port_num))
            s.send("INFO\r\n".encode('utf-8'))
            result = s.recv(1024).decode('utf-8')
            if "redis_version" in result:

                command = "redis-cli -h %s -p %s" % (ip, port.port_num)
                res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                res.stdin.write(b'info \n')
                out, err = res.communicate()
                out = out.decode('utf-8')
                desc = 'info:\n' + str(out)
                Risk.objects.update_or_create(port=port, defaults={'asset': port.asset,
                                                                   'risk_type': 'redis空口令',
                                                                   'desc': desc
                                                                   })

                logger.info('[$$$]success')

            elif "Authentication" in result:
                for pass_ in passwords:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, 6379))
                    s.send(("AUTH %s\r\n" % pass_).encode('utf-8'))
                    result = s.recv(1024).decode('utf-8')
                    if '+OK' in result:
                        Risk.objects.update_or_create(port=port, defaults={'asset': port.asset,
                                                                           'risk_type': 'redis弱口令',
                                                                           'desc': '弱密码 %s' % pass_
                                                                           })

        except Exception as e:
            logger.error(e)
