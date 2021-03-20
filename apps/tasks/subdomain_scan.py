from celery import shared_task
import subprocess
from apps.webapps.models import WebApp, Domain
import socket
import requests
import urllib3
from apps.tasks.asset_discovery import get_ip_info
from django.conf import settings
from django.db.models import Q
from apps.assets.models import Asset
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool
import time
from lib.common import check_waf

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()


@shared_task
def start(task):
    """
    如果目标是 “*”， 扫描所有子域名；
    如果是手工输入的域名列表，如果数据库中没有，先存入，再扫描子域名；
    """
    task_target = task.target
    targets = []
    if task_target == '*':
        domains = Domain.objects.exclude(in_scope='no')
        for domain in domains:
            targets.append(domain.domain)
    else:
        _targets = task_target.strip().replace('，', ',').split(',')
        for target in _targets:
            target = target.strip()
            targets.append(target)

    denominator = len(targets)
    molecular = 0
    for target in targets:
        molecular += 1
        logger.info('-' * 75)
        logger.warning('[子域名扫描] %s' % target)
        ips = []
        domains = Domain.objects.filter(domain=target)
        if domains.exists():
            domain = domains[0]
        else:
            domain = Domain.objects.create(domain=target, platform=task.platform)

        subdomains = get_subdomains_virustotal(target)
        if not subdomains:
            logger.error('virustotal api 未查询到域名')

        subdomains2 = get_subdomains_subfinder(target)
        if subdomains2:
            for s in subdomains2:
                if s not in subdomains:
                    subdomains.append(s)

        webapps = WebApp.objects.filter(Q(domain=target) & Q(source=1))  # 1是手工添加的子域名
        # 因为有些域名是扫描不出来的，需要手工添加到数据库。跟扫描出来的子域名合在一起，执行后面操作
        if webapps:
            for webapp in webapps:
                subdomains.append(webapp.subdomain)
                ips.append(webapp.ip)
        if not subdomains:
            logger.debug('未扫描到子域名')
            continue

        logger.debug('发现%d个子域名' % len(subdomains))

        try:
            pool = ThreadPool(15)
            _subdomains = [(target, subdomain) for subdomain in subdomains]
            ips2 = pool.map(check_subdomain_is_exist, _subdomains)
            if ips2:
                ips = ips + ips2
            pool.close()
            pool.join()
        except Exception as e:
            logger.critical(e)

        try:
            while '' in ips:
                ips.remove('')
            while None in ips:
                ips.remove(None)
            ips = list(set(ips))

        except Exception as e:
            logger.critical(e)
        if ips:
            logger.debug('Found %d hosts: ' % len(ips))
            logger.debug(ips)

            for ip in ips:
                try:
                    Asset.objects.get(ip=ip)
                except:
                    get_ip_info(ip)
        subdomains_total = WebApp.objects.filter(domain=target)
        domain.subdomains_total = len(subdomains_total)
        domain.save()

        if molecular == denominator:
            percent = 100.0
            logger.warning('%s [%d/%d]' % (str(percent) + '%', molecular, denominator))
        else:
            percent = round(1.0 * molecular / denominator * 100, 2)
            logger.warning('%s [%d/%d]' % (str(percent) + '%', molecular, denominator))

    logger.warning('子域名扫描完毕')


def check_subdomain_is_exist(p):
    """
    检测域名是否已出入数据库，如果已存在，跳过，如果没有，进一步获取详细信息
    :param p:
    :return:
    """
    target = p[0]
    subdomain = p[1]
    if 'status' in subdomain:
        return
    try:
        WebApp.objects.get(subdomain='https://' + subdomain)
        logger.debug('[Existed] %s' % subdomain)
        return
    except:
        ip = get_subdomain_info(target, subdomain)
        return ip


def get_subdomains_virustotal(target):
    subdomains = []

    API_KEY = "61c48fcc9b6d2a6181e738d215c37290f395293b4a0daa9da74f0b181431e307"
    url = "http://www.virustotal.com/vtapi/v2/domain/report"

    params = {"domain": target, "apikey": API_KEY}
    try:
        while True:
            res = requests.get(url, params=params, timeout=10)
            status_code = res.status_code
            if status_code == 200:
                if res.json():
                    subdomains = res.json()['subdomains']
                break
            elif status_code == 204:
                logger.error('The virustotal api request frequency limit')
                time.sleep(5)
    except Exception as e:
        logger.critical(e)

    return subdomains


def get_subdomains_subfinder(target):
    subdomains = []
    c = 'subfinder -o /tmp/%s -d %s' % (target, target)
    try:
        p = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        with open("/tmp/" + target, 'r') as f:
            lines = f.readlines()
            for line in lines:
                subdomains.append(line.strip())
    except Exception as e:
        logger.critical(target + ': ' + str(e))

    return subdomains


def get_subdomain_info(target, subdomain):
    try:
        _subdomain = 'https://' + subdomain
        r = requests.get(_subdomain, headers=settings.HTTP_HEADERS, timeout=30, verify=False, allow_redirects=False)
        port_num = 443
    except:
        logger.error('[Failed] %s' % subdomain)
        return

    if r.text:
        status_code = r.status_code
        if status_code not in settings.WORTHY_HTTP_CODE:
            logger.error('[%s] %s' % (status_code, subdomain))
            return
        try:
            if int(r.headers["Content-Length"]) < 100:
                return
        except:
            pass
        if 'Welcome to OpenResty' in r.text:
            return
        if 'Welcome to nginx' in r.text:
            return
        if 'Thank you for using tengine' in r.text:
            return
        # if status_code == 500:
        #     if 'cloudflare' in r.text:
        #         logger.error('[%s] %s, cloudflare' % (status_code, subdomain))
        #         return
        # if status_code in [301, 302]:
        #     location = r.headers['location']
        #     logger.debug('Location: ' + location)
        #     if subdomain != location.split('//')[1].split('/')[0]:
        #         return

        try:
            cmd = 'whatweb %s --colour never' % _subdomain
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            other_info = out.decode('utf-8')
        except Exception as e:
            logger.critical(subdomain + ': ' + str(e))
            other_info = None
        waf = check_waf(r.headers, r.text)

        if waf:
            logger.debug('WAF or CDN:' + str(waf))
            ip = None
        else:
            ip = socket.gethostbyname(_subdomain.split('//')[-1].split(':')[0])

        try:
            server = r.headers['server']

        except Exception as e:
            server = None
            logger.error(e)
        try:
            WebApp.objects.update_or_create(domain=target, subdomain=_subdomain, defaults={'ip': ip,
                'status_code': status_code, 'server': server, 'waf': waf, 'other_info': other_info, 'port': port_num
            })
            logger.info('[GET] ' + _subdomain)
        except Exception as e:
            logger.critical(e)

        return ip
    else:
        logger.error('[None] %s' % subdomain)
        return None


def subdomain_scan(task):
    start.delay(task)
