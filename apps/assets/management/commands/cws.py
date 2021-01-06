"""
检查web存活状态
"""
from django.core.management.base import BaseCommand
from apps.assets.models import Asset
from apps.webapps.models import WebApp
import requests
from django.conf import settings
from apps.tasks.asset_discovery import get_ip_info


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('- 检查web存活状态 ...')
        webapps = WebApp.objects.all()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
        }

        for webapp in webapps:
            print('-' * 75)
            print('+ Scan: ' + webapp.subdomain)
            try:
                requests.get(webapp.subdomain, headers=headers, timeout=10, verify=False, allow_redirects=False)
                print('+ 访问正常')
            except Exception as e:
                webapp.delete()
                print('- 删除成功')
                continue
