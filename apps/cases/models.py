from django.db import models
from mdeditor.fields import MDTextField


class CaseField(models.Model):
    name = models.CharField(max_length=100, unique=True, default='', verbose_name='用例领域')
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
    name = models.CharField(max_length=100, unique=True, default='', verbose_name='漏洞名称')
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    level = models.CharField(choices=level_choice, default='high', verbose_name='危害等级', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'漏洞分类'
        verbose_name_plural = verbose_name


class FunctionPoint(models.Model):
    name = models.CharField(max_length=100, verbose_name='功能点')
    f_field = models.ForeignKey(CaseField, on_delete=models.CASCADE, verbose_name='所属领域', default='')
    vuls = models.ManyToManyField(Vul, verbose_name='可能存在漏洞', blank=True, max_length=255)
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'功能点'
        verbose_name_plural = verbose_name


class Case(models.Model):
    type_choice = (
        ('general', '通用用例'),
        ('special', '专用用例'),
    )
    case_field = models.ForeignKey(CaseField, on_delete=models.CASCADE, verbose_name='用例领域')
    vul = models.ForeignKey(Vul, on_delete=models.CASCADE, verbose_name='所属漏洞')
    type = models.CharField(choices=type_choice, default='general', verbose_name='用例类型', max_length=10)
    function_point = models.ForeignKey(FunctionPoint, on_delete=models.CASCADE, verbose_name='所属功能点', default=None, null=True, blank=True)
    content = MDTextField(verbose_name='用例内容', default='', blank=True, null=True)
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = u'测试用例'
        verbose_name_plural = verbose_name


