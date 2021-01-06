from django.core.management.base import BaseCommand
import nmap
from apps.assets.models import Asset, Port, Software
import subprocess
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('开始扫描所有资产开启的服务...')
        nm = nmap.PortScanner()
        assets = Asset.objects.filter(scanned='no')

        for asset in assets:
            # if asset.port_set.all():
            #     continue
            print('-' * 100)
            ip = asset.ip
            try:
                print(ip)
                cmd = 'masscan -p0-65535 --rate 15000 -oJ /opt/warden/warden/tmp.json %s' % ip
                p = subprocess.Popen(cmd, shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                out, err = p.communicate()
                if err:
                    print('扫描出错了：' + err)
                    continue
                ports = list()
                with open('/opt/warden/warden/tmp.json') as f:
                    portsL = f.read().split('\n')[0:-2]
                    if len(portsL) > 100:
                        print('port num too much')
                        asset.scanned = 'yes'
                        asset.save()
                        continue
                    for i in portsL:
                        i = i.strip(',')
                        port_dict = json.loads(i)
                        port = port_dict['ports'][0]['port']
                        ports.append(str(port))

                try:
                    ports.remove('80')
                except:
                    pass
                try:
                    ports.remove('443')
                except:
                    pass

                if ports:
                    ports = list(set(ports))
                    print(ports)
                    try:
                        nm.scan(ip, ports=','.join(ports), arguments='-A -Pn -sS --open --host-timeout 30m')
                        ports_dict = nm[ip]['tcp']
                    except Exception as e:
                        print(e)
                        continue
                    for k, v in ports_dict.items():
                        try:
                            Software.objects.get(nmap_name=v['product'])
                        except Exception as e:
                            print(e)
                            Software.objects.create(nmap_name=v['product'])

                        try:
                            Port.objects.update_or_create(asset_id=asset.id, port_num=k,
                                                          defaults={'software_name': v['product'],
                                                                    'software_version': v['version'],
                                                                    'service_name': v['name']})
                        except Exception as e:
                            print(e)
                        print(str(k) + ' ' + str(v['product']) + ' ' + str(v['name']) + ' ' + str(v['version']))
                else:
                    print('Not found open port')
                asset.scanned = 'yes'
                asset.save()
            except Exception as e:
                print(e)

        print('任务完成！')
