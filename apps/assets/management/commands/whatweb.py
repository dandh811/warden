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
        print('update whatweb info')
        try:
            webapps = WebApp.objects.all()
            for webapp in webapps:
                subdomain = webapp.subdomain
                print('[Scan] %s' % subdomain)
                try:
                    cmd = 'whatweb %s --colour never' % subdomain
                    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = p.communicate()
                    other_info = out.decode('utf-8').replace(',', ',\n')
                    webapp.other_info = other_info
                    webapp.save()
                except Exception as e:
                    print(subdomain + ': ' + str(e))
        except Exception as e:
            print(str(e))