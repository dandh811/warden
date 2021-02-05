from django.core.management.base import BaseCommand
from apps.assets.models import Port
from lxml.html import fromstring
from apps.webapps.models import WebApp
import urllib3
from django.conf import settings
import requests
import subprocess
from loguru import logger
import sys

urllib3.disable_warnings()


headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,[i]/[/i];q=0.8",
        # "Accept-Encoding": "gzip, deflate, sdch"
    }


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info('- Get webapps from assets')
        ports = Port.objects.filter(service_name__icontains='http').order_by('-id')

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

                logger.info('+ Get URL info: ' + _subdomain)

                try:
                    r = requests.get(_subdomain, headers=headers, timeout=10, verify=False, allow_redirects=False)
                except Exception as e:
                    logger.info('* Access error, skip this subdomain')
                    continue

                if r.text:
                    status_code = r.status_code

                    if status_code not in settings.WORTHY_HTTP_CODE:
                        logger.info('* Response %s, ignore this subdomain' % status_code)
                        continue

                    command = 'whatweb %s' % _subdomain
                    p = subprocess.Popen(command, shell=True,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.STDOUT)
                    out, err = p.communicate()
                    other_info = out.decode('utf-8')
                    try:
                        server = r.headers['server']
                        tree = fromstring(r.text.encode('utf-8'))

                        logger.info('+ Server: ' + str(server))
                    except Exception as e:
                        server = ''
                    try:
                        WebApp.objects.update_or_create(domain=domain, subdomain=_subdomain, defaults={'ip': ip,
                            'status_code': status_code, 'server': server, 'headers': r.headers,
                            'waf': '', 'other_info': other_info, 'port': port_num})

                        logger.info('+ Valid Subdomain: \033[0;32m %s \033[0m' % _subdomain)
                    except Exception as e:
                        print(e)

        logger.info('+ Task done')
