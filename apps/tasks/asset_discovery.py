import nmap
from apps.assets.models import Asset, Port, Software
from celery import shared_task
import subprocess
import json
from django.conf import settings
import requests
from lxml.html import fromstring
from apps.webapps.models import WebApp
from loguru import logger


def nmap_port(host, port):
    """扫描指定端口"""
    nm = nmap.PortScanner()
    nm.scan(host, port)
    if nm[host].state() == 'up':
        return nm[host]['tcp'][port]


def nmap_host_all(host):
    """ 全端口扫描 """
    nm = nmap.PortScanner()
    nm.scan(host, '1-65535')
    if nm[host].state() == 'up':
        return nm[host]['tcp']


def nmap_alive_lists(target):
    hosts_list = [host.strip() for host in target.split(',')]

    nm = nmap.PortScanner()
    survive = []
    for hosts in hosts_list:
        nm.scan(hosts=hosts, arguments='-sP')
        # -n 表示，
        # -Pn 跳过ping，直接扫描；
        # -sP ping扫描
        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                survive.append(host)

    return survive


def add_nmap_scan(target):
    logger.info('%-30s%-30s' % ('[+] 扫描:', target))
    res = nmap_alive_lists(target)

    return res


def get_ip_info(ip):
    logger.info('-'*75)
    logger.debug('扫描: ' + ip)
    try:
        Asset.objects.get(ip=ip)
    except Exception as e:
        asset = Asset.objects.create(ip=ip)
    cmd = 'masscan -p0-65535 --rate 500 -oJ /opt/warden/warden/tmp.json %s' % ip
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret = p.wait()
    command_output = p.stdout.read().decode('utf-8')
    if ret != 0:
        logger.critical('[*] ' + command_output)
        logger.critical(command_output)
        return

    ports = []
    with open('/opt/warden/warden/tmp.json') as f:
        portsL = f.read().split('\n')[0:-2]
        if len(portsL) > 100:
            return
        for i in portsL:
            i = i.strip(',')
            try:
                port_dict = json.loads(i)
                port = port_dict['ports'][0]['port']
                ports.append(str(port))
            except Exception as e:
                logger.error(e)

    logger.info(ports)
    try:
        ports.remove('80')
    except Exception as e:
        logger.critical(e)
    try:
        ports.remove('443')
    except Exception as e:
        logger.critical(e)

    if ports:
        nm = nmap.PortScanner()
        ports = list(set(ports))   # 端口去重处理

        nm.scan(ip, ports=','.join(ports), arguments='-A -Pn -sS --open --host-timeout 30m')
        try:
            ports_dict = nm[ip]['tcp']
        except:
            return
        for k, v in ports_dict.items():
            if v['name'] in ['tcpwrapped', 'unknown', 'dnox', 'infowave', 'amberon', 'tnp1-port']:
                continue
            if v['name']:
                if v['product']:
                    Software.objects.update_or_create(nmap_name=v['product'])

                try:
                    Port.objects.update_or_create(asset=asset, port_num=k,
                                              defaults={'software_name': v['product'],
                                                        'software_version': v['version'],
                                                        'service_name': v['name']})
                    # if 'http' in v['name'] and k not in [80, 443]:
                    #     get_web_info(ip, str(k))
                except Exception as e:
                    logger.critical(e)
                logger.info(str(k) + ', ' + str(v['product']) + ', ' + str(v['name']) + ', ' + str(v['version']))
        asset.scanned = 'yes'
        asset.save()
    else:
        logger.info('除80，443，未开启其他端口')


def get_web_info(ip, port):
    url = 'https://' + ip + ':' + str(port)
    logger.info('-' * 75)

    logger.debug('scan:' + url)

    try:
        r = requests.get(url, headers=settings.HTTP_HEADERS, timeout=10, verify=False, allow_redirects=False)
    except Exception as e:
        logger.critical(e)
        try:
            url = 'http://' + ip + ':' + str(port)
            r = requests.get(url, headers=settings.HTTP_HEADERS, timeout=30, verify=False, allow_redirects=False)
        except:
            logger.error('[访问失败]http://%s' % url)
            return

    if r.text:
        status_code = r.status_code

        if status_code not in settings.WORTHY_HTTP_CODE:
            logger.critical('返回 %s, 忽略该web' % status_code)
            return

        command = 'whatweb %s' % url
        p = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        out, err = p.communicate()
        other_info = out.decode('utf-8')
        try:
            server = r.headers['server']
            tree = fromstring(r.text.encode('utf-8'))

            logger.info('%-30s%-30s' % ('[+] Server:', str(server)))
        except Exception as e:
            server = ''
        try:
            WebApp.objects.update_or_create(subdomain=url, defaults={'domain': ip, 'ip': ip,
                                                                       'status_code': status_code,
                                                                       'server': server,
                                                                       'headers': r.headers,
                                                                       'waf': '',
                                                                       'other_info': other_info,
                                                                       'port': port})

            logger.info('%-30s%-30s' % ('[+] Valid:', 'True'))
        except Exception as e:
            print(e)


def nmap_call(task, nm_a):
    ips = add_nmap_scan(task.target)

    logger.info('发现存活主机数：' + str(len(ips)))
    ips = reversed(ips)
    if task.policy == 'increase':
        for ip in ips:
            try:
                asset = Asset.objects.get(ip=ip)
                if asset.scanned == 'yes':
                    continue
                else:
                    get_ip_info(ip)
            except Exception as e:
                Asset.objects.create(ip=ip)
                get_ip_info(ip)

    else:
        for ip in ips:
            try:
                get_ip_info(ip)
            except Exception as e:
                logger.critical(e)
    while nm_a.still_scanning():
        nm_a.wait(2)

    logger.info('-' * 75)


def asset_discovery(task):
    """ 调用python-nmap模块进行扫描 """
    nm = nmap.PortScanner()
    nm_a = nmap.PortScannerAsync()

    start.delay(task, nm_a)


@shared_task
def start(task, nm_a):
    nmap_call(task, nm_a)
