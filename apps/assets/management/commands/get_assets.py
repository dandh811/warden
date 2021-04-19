from apps.assets.models import Asset, Port, Software
from django.db.models import Q, Count
from django.core.management.base import BaseCommand
from django.conf import settings
import requests
import csv
import re
import nmap


class Command(BaseCommand):
    help = "从安全态势感知平台提取资产信息"

    def handle(self, *args, **options):
        print(help)
        get_assets()

        print('+ 任务完成')


def get_assets():
    with open('/home/secscan/assets.csv', 'rt', encoding="GB2312") as f:
        cr = csv.reader(f)
        for row in cr:
            print('-' * 90)
            try:
                if '终端' in row[10]:
                    continue
                ip = row[0].strip('\'')
                print(ip)

                group = row[1].strip('\'')
                hostname = row[3].strip('\'')
                ports = re.findall(r'\d+', row[12])
                os = row[13].strip('\'')

                print(ports)

                Asset.objects.update_or_create(ip=ip, defaults={"group": group, "hostname": hostname,
                                                                "os": os})
            except Exception as e:
                print(e)
                continue

            if ports:
                asset = Asset.objects.get(ip=ip)
                res = Port.objects.filter(asset=asset)
                if res:
                    continue
                nm = nmap.PortScanner()

                nm.scan(ip, ports=','.join(ports), arguments='-Pn -sV --open --host-timeout 30m')
                # -A 参数可以扫描服务版本号
                try:
                    ports_dict = nm[ip]['tcp']
                except Exception as e:
                    print(e)
                    continue
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
                        except Exception as e:
                            print(e)
                        print(
                            str(k) + ', ' + str(v['product']) + ', ' + str(v['name']) + ', ' + str(v['version']))
