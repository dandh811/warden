from apps.assets.models import Asset, Port, Software
from apps.webapps.models import WebApp
from django.db.models import Q
from celery import shared_task
import uuid
import os
import hashlib
from django.core.management.base import BaseCommand
import datetime
import requests
from django.conf import settings
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('开始清理无用端口...')

        ports = Port.objects.order_by('id')

        for port in ports:
            try:
                port.asset
            except Exception as e:
                print(e)

                print('无用资产：', port.id)
                port.delete()

        print('任务完成！')
