# ***********************************************
# @Time    : 2019/8/26 13:13
# @Author  : dandh811
# @Blog    ：https://www.xiuxing128.top
# ***********************************************

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import django.utils.timezone as timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from apps.tasks.models import Task


class Exploit(models.Model):
    exploit_choice = (
        ('url_illegal_redirect', 'URL非法重定向'),
    )

    id = models.AutoField(primary_key=True)
    source_host = models.CharField(max_length=64, default='', verbose_name="来源", blank=True)
    type = models.CharField(choices=exploit_choice, max_length=64, default='', verbose_name="类型")
    path = models.CharField(default='online', max_length=255, verbose_name='path')
    full_path = models.CharField(default='online', max_length=255, verbose_name='full_path')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
