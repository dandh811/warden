from django.db import models
import django.utils.timezone as timezone


class CaseField(models.Model):
    name = models.CharField(max_length=100, unique=True, default='', verbose_name='用例领域')
    desc = models.TextField(default='', verbose_name="备注", null=True, blank=True)
    c_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'用例领域'
        verbose_name_plural = verbose_name


class Vul(models.Model):
    level_choice = (
        ('high', 'high'),
        ('middle', 'middle'),
        ('low', 'low',)
    )
    name = models.CharField(max_length=100, unique=True, default='', verbose_name='漏洞分类')
    desc = models.TextField(default='', verbose_name="备注", null=True, blank=True)
    c_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    level = models.CharField(choices=level_choice, default='high', verbose_name='危害等级', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'漏洞分类'
        verbose_name_plural = verbose_name


class Case(models.Model):
    name = models.CharField(max_length=100, verbose_name='用例名称')
    content = models.TextField(verbose_name='用例内容', default='', blank=True, null=True)
    case_field = models.ForeignKey(CaseField, on_delete=models.CASCADE, verbose_name='用例领域')
    vul = models.ForeignKey(Vul, on_delete=models.CASCADE, verbose_name='归属漏洞')
    c_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    desc = models.TextField(verbose_name="备注", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'测试用例'
        verbose_name_plural = verbose_name
