from apps.assets.models import Port, Risk
import socket
import subprocess
timeout = 2
from lib.wechat_notice import wechat
from loguru import logger

plugin = 'rsync'


def start(**kwargs):
    policy = kwargs['policy']
    assets = kwargs['assets']
    ports = Port.objects.filter(asset_id__in=assets, service_name__icontains='rsync')
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
    for port in ports:
        ip = port.asset.ip
        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))

        try:
            payload = b"\x40\x52\x53\x59\x4e\x43\x44\x3a\x20\x33\x31\x2e\x30\x0a"
            socket.setdefaulttimeout(timeout)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (ip, port.port_num)
            sock.connect(server_address)
            sock.sendall(payload)
            initinfo = sock.recv(400)
            if b"RSYNCD" in initinfo:
                sock.sendall(b"\x0a")
            modulelist = sock.recv(200)
            sock.close()
            if len(modulelist) > 0:
                command = 'rsync -v rsync://%s:%s' % (ip, port.port_num)
                p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                out, err = p.communicate()
                out = out.decode('utf-8')
                desc = 'rsync空口令，连接上服务后，获取到如下信息:\n' + str(out)
                Risk.objects.update_or_create(target=ip + ':' + str(port.port_num), risk_type='rsync',
                                              defaults={'desc': desc})
                logger.info('[$], this host is vulnerable')
        except Exception as e:
            logger.error(e)
