from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjectSettings.settings')
app = Celery('blog')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# # kafka 监控任务，在celery任务中执行
# topic = "kbunting"
# bootstrap_servers = ['52.80.208.149:8000']
# api_version = (0, 10)
#
# from TaskManage.tasks import kafka_server
# kafka_server.delay(topic, bootstrap_servers, api_version)
