from django.db import models
from django.contrib.auth.models import User
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


class XssPrey(models.Model):
    domain = models.CharField(max_length=64, default='', verbose_name="域名")
    user_agent = models.CharField(max_length=255, default='', verbose_name="user_agent")
    cookie = models.TextField(default='', verbose_name="cookie")
    ip = models.TextField(verbose_name="IP", blank=True, null=True, default='')

    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.domain

    class Meta:
        ordering = ['domain']
        verbose_name = 'XSS猎物'
        verbose_name_plural = verbose_name