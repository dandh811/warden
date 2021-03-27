import socket
from apps.assets.models import Risk, Port
from lib.wechat_notice import wechat
from loguru import logger

plugin = 'docker'


def start(**kwargs):
    policy = kwargs['policy']

    socket.setdefaulttimeout(2)
    ports = Port.objects.filter(service_name__icontains='docker')
    if not ports:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))

    for port in ports:
        port_num = port.port_num
        ip = port.asset.ip

        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port_num))
            payload = "GET /containers/json HTTP/1.1\r\nHost: %s:%s\r\n\r\n" % (ip, port_num)
            s.send(payload.encode())
            recv = s.recv(1024)
            if b"HTTP/1.1 200 OK" in recv and b'Docker' in recv and b'Api-Version' in recv:
                logger.info('%-30s%-30s' % ('[$$$]success, ', "[True], this host is vulnerable"))
                desc = 'Docker未授权访问漏洞，获取到如下信息：\n' + str(recv)
                Risk.objects.update_or_create(target=ip, risk_type='docker未授权访问', defaults={'desc': desc})
                title = 'docker未授权访问'
                content = desc
                wechat.send_msg(title, content)
        except Exception as e:
            logger.error(e)
