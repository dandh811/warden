from django.db import models

yes_or_no = (
    ('yes', '是'),
    ('no', '否')
)

platform_list = (
    ('hackerone', 'hackerone'),
    ('bugcrowd', 'bugcrowd'),
    ('BountyFactory', 'BountyFactory'),
    ('Intigriti', 'Intigriti'),
    ('Bugbountyjp', 'Bugbountyjp'),
    ('Safehats', 'Safehats'),
    ('BugbountyHQ', 'BugbountyHQ'),
    ('Hackerhive', 'Hackerhive'),
    ('Hackenproof', 'Hackenproof'),
    ('other', '其他'),
)


class Domain(models.Model):
    domain = models.CharField(max_length=100, unique=True, default='')
    company = models.CharField(max_length=100, null=True, verbose_name='公司', blank=True)
    s_url = models.CharField(max_length=250, null=True, verbose_name='源URL', blank=True)
    desc = models.CharField(max_length=200, default='', verbose_name="备注", null=True, blank=True)
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    platform = models.CharField(choices=platform_list, max_length=100, null=True, verbose_name='众测平台', default='hackerone')
    scanned = models.CharField(max_length=100, null=True, verbose_name='是否已扫描', blank=True, default='not')
    in_scope = models.CharField(choices=yes_or_no, default='yes', max_length=5, verbose_name='是否在测试范围内')
    subdomains_total = models.IntegerField(verbose_name='子域名数量', blank=True, null=True, default=0)

    def __str__(self):
        return '%s %s' % (self.domain, self.company)

    class Meta:
        verbose_name = u'根域名'
        verbose_name_plural = verbose_name


class WebApp(models.Model):
    source_choice = (
        (1, '手工添加'),
        (2, '扫描发现'),
        (3, '其他',)
    )
    status_choice = (
        ('online', '在线'),
        ('indeterminate', '不确定')
    )
    domain = models.CharField(max_length=100, null=True, blank=True)
    subdomain = models.CharField(max_length=200, unique=True, default='')
    manual = models.CharField(choices=yes_or_no, verbose_name='是否已手工分析', default='no', max_length=3)

    status_code = models.CharField(default='', verbose_name='状态码', max_length=10)
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    source = models.IntegerField(choices=source_choice, default=2, verbose_name='来源')
    server = models.CharField('web server', max_length=250, null=True, blank=True)
    ip = models.CharField(max_length=64, verbose_name="IP", blank=True, null=True, default='')
    port = models.CharField(max_length=5, verbose_name="端口号", blank=True, null=True, default='')
    waf_or_cdn = models.CharField('WAF or CDN', max_length=250, null=True, blank=True)
    other_info = models.TextField(verbose_name='其他信息', default='', blank=True, null=True)
    report = models.CharField(null=True, default='', max_length=200, blank=True)
    comment = models.TextField(verbose_name="备注", null=True, blank=True)
    in_scope = models.CharField(choices=yes_or_no, default='yes', max_length=5, verbose_name='是否在测试范围内')
    scanned = models.CharField(max_length=250, null=True, verbose_name='是否已扫描', blank=True, default='not')
    status = models.CharField(choices=status_choice, default='online', max_length=20, verbose_name='状态')
    awvs_scanned = models.CharField(choices=yes_or_no, default='no', max_length=20, verbose_name='是否awvs扫描完成')

    def __str__(self):
        return self.subdomain

    class Meta:
        verbose_name = u'子域名'
        verbose_name_plural = verbose_name


class WebUrls(models.Model):
    url = models.TextField(unique=True)
    webapp = models.ForeignKey(WebApp, on_delete=models.CASCADE)
    manual = models.BooleanField(verbose_name='是否已手工分析', default=False)

    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    scanned = models.CharField(max_length=200, null=True, verbose_name='是否已扫描', blank=True, default='not')

    def __str__(self):
        return '%s %s' % (self.url, self.webapp.domain)

    class Meta:
        verbose_name = u'URL列表'
        verbose_name_plural = verbose_name
