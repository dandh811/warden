"""
检查资产存活状态
先通过ping IP，如果通说明存活；如果不通在与资产的开放端口建立连接，如果都无法建立连接，说明资产不存活；
"""
from django.core.management.base import BaseCommand
from apps.assets.models import Asset
from apps.webapps.models import WebApp, Domain
import requests
from django.conf import settings
from apps.tasks.asset_discovery import get_ip_info
from apps.tasks.asset_discovery import nmap_alive_lists
import subprocess
import socket


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('- 检查资产存活状态 ...')
        # assets = Asset.objects.all()
        assets = []

        for asset in assets:
            print('-' * 75)
            ip = asset.ip

            print('+ Scan: ' + ip)
                # process = subprocess.Popen('ping -c 1 %s' % ip, stdout=subprocess.PIPE, shell=True)
                # out, err = p.communicate()
                # command_output = out.decode('utf-8')
                #
                # if res == 0:
                #     print('+ 可以ping通，资产存活')
                # else:
                #     print('* ping不通，尝试连接端口 ...')
            ports = asset.port_set.all()
            if not ports:
                continue

            exists = False
            for port in ports:
                sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sk.settimeout(3)
                try:
                    sk.connect((ip, port.port_num))  # port.port_num 默认就是int型数据
                    exists = True
                except Exception as e:
                    print("%s not open" % port.port_num)
                    port.delete()
                sk.close()

            if not exists:
                asset.delete()
                print('* 资产不存活，删除成功')
        webapps = WebApp.objects.all()
        for webapp in webapps:
            domain = webapp.domain
            try:
                Domain.objects.get(domain=domain)
            except Exception as e:
                print(domain)
                webapp.delete()
        print('- 任务结束')

