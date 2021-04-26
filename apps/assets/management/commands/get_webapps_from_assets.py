from django.core.management.base import BaseCommand
from apps.assets.models import Port
from lxml.html import fromstring
from apps.webapps.models import WebApp
import urllib3
from django.conf import settings
import requests
from loguru import logger
import re
import subprocess

urllib3.disable_warnings()


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('从资产端口获取web系统')
        # webs = WebApp.objects.all()
        # for web in webs:
        #     subdomain = web.subdomain
        #     try:
        #         r = requests.get(subdomain, headers=settings.HTTP_HEADERS, timeout=15, verify=False,
        #                          allow_redirects=True)
        #     except:
        #         logger.error('[访问失败] %s' % subdomain)
        #         web.delete()
        #         continue
        #
        #     if r.text:
        #         try:
        #             if int(r.headers["Content-Length"]) < 100:
        #                 logger.info('返回内容长度不够100')
        #                 web.delete()
        #         except:
        #             pass
        #         if 'Welcome to OpenResty' in r.text:
        #             logger.info('Welcome to OpenResty')
        #             web.delete()
        #         if 'Welcome to nginx' in r.text:
        #             logger.info('Welcome to nginx')
        #             web.delete()
        #         if 'Thank you for using tengine' in r.text:
        #             logger.info('Thank you for using tengine')
        #             web.delete()
        #         if 'ilo:' in r.text:
        #             logger.info(subdomain)
        #             web.delete()
        #         if 'root.title' in r.text:
        #             logger.info(subdomain)
        #             web.delete()
        #         title = re.findall('<title>(.+)</title>', r.text)
        #         logger.info(title)
        #######################################################################################
        ports = Port.objects.filter(service_name__icontains='http')

        for port in ports:
            ip = port.asset.ip
            port_num = port.port_num

            res = WebApp.objects.filter(ip=ip, port=port_num)
            if res:
                continue
            res2 = WebApp.objects.filter(ip=ip)
            if res2:
                domain = res2[0].domain
            else:
                domain = ''

            schemas = ['http', 'https']
            for schema in schemas:
                _subdomain = schema + '://' + ip + ':' + str(port_num)
                logger.info('-' * 75)

                logger.info('获取web信息: ' + _subdomain)

                try:
                    r = requests.get(_subdomain, headers=settings.HTTP_HEADERS, timeout=15, verify=False, allow_redirects=True)
                except Exception as e:
                    logger.info(e)
                    continue

                if r.text:
                    status_code = r.status_code
                    if status_code != 200:
                        continue
                    try:
                        if int(r.headers["Content-Length"]) < 100:
                            logger.info('返回内容长度不够100')
                            continue
                    except:
                        pass
                    if 'Welcome to OpenResty' in r.text:
                        logger.info('Welcome to OpenResty')
                        continue
                    if 'Welcome to nginx' in r.text:
                        logger.info('Welcome to nginx')
                        continue
                    if 'Thank you for using tengine' in r.text:
                        logger.info('Thank you for using tengine')
                        continue
                    if 'ilo:' in r.text:
                        continue
                    if 'root.title' in r.text:
                        continue
                    try:
                        title = re.findall('<title>(.*?)</title>', r.text)
                        title = title[0]
                        logger.info(title)
                    except:
                        title = ''
                    command = 'whatweb %s --colour never' % _subdomain
                    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    out, err = p.communicate()
                    try:
                        other_info = out.decode('utf-8')
                    except:
                        other_info = out.decode('gb2312')
                    try:
                        server = r.headers['server']
                        tree = fromstring(r.text.encode('utf-8'))

                        logger.info('+ Server: ' + str(server))
                    except Exception as e:
                        server = ''
                    try:
                        WebApp.objects.update_or_create(domain=domain, subdomain=_subdomain, defaults={'ip': ip,
                            'status_code': status_code, 'server': server, 'title': title,
                            'waf': '', 'other_info': other_info, 'port': port_num})

                        logger.info('+ 有效web: %s' % _subdomain)
                    except Exception as e:
                        print(e)

        logger.info('+ Task done')
