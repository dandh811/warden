from django.db import models
import django.utils.timezone as timezone
from django.urls import reverse

yes_or_no = (
    ('yes', '是'),
    ('no', '否')
)


class Asset(models.Model):
    id = models.AutoField(primary_key=True)
    memo = models.TextField(null=True, blank=True, verbose_name='备注')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    ip = models.CharField(max_length=15, verbose_name="IP", blank=True, null=True, default='')
    scanned = models.CharField(max_length=10, null=True, verbose_name='是否已扫描', blank=True, default='no')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('assets:asset_detail', kwargs={'asset_id': self.id})


class Port(models.Model):
    id = models.AutoField(primary_key=True)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    port_num = models.IntegerField('端口号', blank=True, null=True)
    software_name = models.CharField('软件名', max_length=128, null=True, default='')
    software_version = models.CharField('软件版本', max_length=100, null=True)
    service_name = models.CharField('服务名', max_length=128, null=True, blank=True)
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    scanned = models.CharField(max_length=200, null=True, verbose_name='是否已扫描', blank=True, default='not')

    def __str__(self):
        return '%s: %s: %s: %s' % (self.asset.ip, self.port_num, self.service_name, self.software_name)

    def get_absolute_url(self):
        return reverse('port_display_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = '端口'
        verbose_name_plural = verbose_name


class Software(models.Model):
    """
    安装软件信息
    """
    type_choice = (
        ('middle_ware', '中间件'),
        ('database', '数据库'),
        ('other', '其它类')
    )

    nmap_name = models.CharField(max_length=64, unique=True, verbose_name='nmap识别名称', null=True)
    s_type = models.CharField(choices=type_choice, default='middle_ware', max_length=30, verbose_name='软件类型')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    comment = models.TextField(verbose_name="备注", null=True, blank=True)

    def __str__(self):
        return '%s' % (self.nmap_name)

    class Meta:
        verbose_name = '安装应用'
        verbose_name_plural = verbose_name
        ordering = ['nmap_name']


class Risk(models.Model):
    status_choice = (
        ('unconfirm', '待确认'),
        ('unfix', '未修复'),
        ('fixed', '已修复'),
        ('ignore', '忽略'),
        ('misreport', '误报'),
    )

    id = models.AutoField(primary_key=True)
    target = models.CharField(null=True, default='', max_length=200)

    risk_type = models.CharField(verbose_name='漏洞类型', default='', null=True, blank=True, max_length=50)
    desc = models.TextField(verbose_name="风险描述", null=True, blank=True)
    bounty = models.IntegerField(verbose_name='赏金($)', default=0, help_text='美元')
    status = models.CharField(verbose_name='状态', choices=status_choice, default='unconfirm', null=True, blank=True, max_length=50)

    comment = models.TextField(verbose_name="备注", null=True, blank=True)
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '风险表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.risk_type


# class Bounty(models.Model):
#     risk = models.ForeignKey("Risk", on_delete=models.CASCADE)