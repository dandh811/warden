from django.db import models
from apps.webapps.models import platform_list


YES_OR_NO = (
    ('y', '是'),
    ('n', '否'),
)

TASK_TYPE = (
    ('asset_discovery', '资产发现'),
    ('subdomain_scan', '域名收集'),
    ('vul_scan', '漏洞扫描'),
)

policy_choose = (
    ('full', '全量扫描'),
    ('increase', '增量扫描'),
)


class Plugins(models.Model):
    name = models.CharField('插件名称', max_length=50, unique=True)
    verbose_name = models.CharField('插件别名', max_length=50)
    tick_status = models.CharField('是否启用', max_length=1, choices=YES_OR_NO, default='y')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '漏洞扫描插件'
        verbose_name_plural = verbose_name


class Task(models.Model):
    name = models.CharField('任务名称', max_length=200)
    type = models.CharField(choices=TASK_TYPE, verbose_name='任务类型', default=None, max_length=100)
    target = models.TextField('被测目标IP或者URL', default='')
    policy = models.CharField(choices=policy_choose, default='increase', max_length=10)
    plugins = models.ManyToManyField(Plugins, verbose_name='漏洞扫描插件', blank=True, max_length=255)
    platform = models.CharField(choices=platform_list, max_length=100, null=True, verbose_name='众测平台', default='hackerone', blank=True)
    des = models.TextField('任务描述信息', null=True, blank=True)
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = verbose_name
        ordering = ['-id']
