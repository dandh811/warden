from django.db import models
from django.contrib.auth.models import User
from apps.tasks.models import Task


class Payload(models.Model):
    payload_choice = (
        ('xss', 'XSS'),
    )

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=64, default='', verbose_name="payload", blank=True)
    type = models.CharField(choices=payload_choice, max_length=64, default='', verbose_name="类型")
    # path = models.CharField(default='online', max_length=255, verbose_name='path')
    # full_path = models.CharField(default='online', max_length=255, verbose_name='full_path')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
