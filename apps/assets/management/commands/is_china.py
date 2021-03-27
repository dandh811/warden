# 根据根域名是否国内的，把对应的子域名和爬取的url也标记为是否国内的

from django.core.management.base import BaseCommand
from apps.assets.models import Asset
from apps.webapps.models import WebApp, Domain, WebUrls
import requests
import subprocess
import socket


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('- 开始任务 ...')

        domains = Domain.objects.filter(is_china=True)

        for domain in domains:
            print('-' * 75)
            print('+ 域名: ' + domain.domain)
            webapps = WebApp.objects.filter(domain=domain.domain)
            if webapps:
                for webapp in webapps:
                    webapp.is_china = True
                    webapp.save()

                    weburls = WebUrls.objects.filter(webapp=webapp)
                    for weburl in weburls:
                        weburl.is_china = True
                        weburl.save()

        print('- 任务结束')

