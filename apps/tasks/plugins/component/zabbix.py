from apps.assets.models import Port, Risk
import socket
from lib.wechat_notice import wechat
import subprocess
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'zabbix'


def start(**kwargs):
    policy = kwargs['policy']
    if policy == 'full':
        ports = Port.objects.filter(service_name__icontains=plugin)
    else:
        ports = Port.objects.filter(service_name__icontains=plugin).exclude(scanned__icontains=plugin)

    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    has_risk = False

    for port in ports:
        ip = port.asset.ip

        try:
            logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))
            socket.setdefaulttimeout(10)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port.port_num))
            s.send("success".encode('utf-8'))
            result = s.recv(1024).decode('utf-8')
            if "Environment" in result:
                logger.info('+ Found Vul: \033[0;32m %s, %s\033[0m' % (ip, str(port.port_num)))

                # command = "redis-cli -h %s -p %s" % (ip, port.port_num)
                # res = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                #                        stderr=subprocess.PIPE)
                # res.stdin.write(b'info \n')
                # out, err = res.communicate()
                # out = out.decode('utf-8')
                # logger.info(out)
                # desc = 'redis空口令，连接上redis后，执行了info命令，读取到如下信息:\n' + str(out)
                desc = 'zabbix未授权访问'
                Risk.objects.update_or_create(target=port.asset.ip, risk_type='zabbix漏洞', defaults={'desc': desc})
                has_risk = True

            # elif "Authentication" in result:
            #     for pass_ in passwords:
            #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #         s.connect((ip, 6379))
            #         s.send(("AUTH %s\r\n" % pass_).encode('utf-8'))
            #         result = s.recv(1024).decode('utf-8')
            #         if '+OK' in result:
            #             Risk.objects.update_or_create(port=port, defaults={'asset': port.asset,
            #                                                                'risk_type': 'redis弱密码',
            #                                                                'desc': '弱密码 %s' % pass_
            #
            #                                                                })
            #             logger.info(ip + ':' + str(port.port_num) + ' 存在弱口令漏洞，密码：%s' % pass_)
            #             has_risk = True
        except Exception as e:
            logger.error(e)

    if has_risk:
        title = '风险提示'
        content = "发现zookeeper漏洞"
        wechat.send_msg(title, content)

    logger.info('-'*100)


vuln = ['zabbix']
