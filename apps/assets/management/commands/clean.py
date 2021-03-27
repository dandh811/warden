# 定期清理僵尸资产和web

from django.core.management.base import BaseCommand
from apps.assets.models import Asset
from apps.webapps.models import WebApp, Domain
import requests
import subprocess
import socket


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('- 检查资产存活状态 ...')
        """
        检查资产存活状态，影响其实不大，几个月检测一次就行；
        先通过ping IP，如果通说明存活；如果不通在与资产的开放端口建立连接，如果都无法建立连接，说明资产不存活；
        """
        assets = Asset.objects.all()

        for asset in assets:
            print('-' * 75)
            ip = asset.ip

            print('+ 扫描: ' + ip)
            p = subprocess.Popen('ping -c 2 %s' % ip, stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            out = out.decode('utf-8')

            if 'ttl=' in out:
                print('+ 可以ping通，资产存活')
            else:
                print('* ping不通，尝试连接端口 ...')
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
                        print("%s 端口未开放" % port.port_num)
                        # port.delete()
                    sk.close()

                if not exists:
                    # asset.delete()
                    print('* 资产不存活，删除成功')

        print('- 检查web存活状态 ...')
        webapps = WebApp.objects.all()
        for webapp in webapps:
            domain = webapp.domain
            try:
                Domain.objects.get(domain=domain)
            except Exception as e:
                print(domain)
                # webapp.delete()
        print('- 任务结束')

