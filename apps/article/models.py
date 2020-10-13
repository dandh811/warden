from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Article(models.Model):
    type_choice = (
        ('share', '分享'),
        ('help', '求助'),
        ('advice', '建议'),
        ('notice', '公告'),

    )
    category_choice = (
        ('scripture', '经文'),
        ('message', '留言'),
        ('notice', '公告'),
        ('music', '音乐'),
    )
    status_choice = (
        ('draft', '草稿'),
        ('published', '发布'),
        ('recycle', '回收站'),
    )
    title = models.CharField(max_length=100, default='', verbose_name="名称")
    desc = models.CharField(max_length=255, default='', verbose_name="简介", blank=True, null=True)
    category = models.CharField(choices=category_choice, null=True, blank=True, verbose_name='分类', max_length=20, default='scripture')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    support = models.IntegerField(default=0, verbose_name='点赞数', null=True, blank=True)
    content = models.TextField('经文', default='', blank=True, null=True)
    voice = models.FileField(upload_to='./voices', default='', blank=True, null=True)
    cover = models.ImageField(upload_to='./article_images', default='', blank=True, null=True)
    status = models.CharField(choices=status_choice, null=True, blank=True, verbose_name='状态', max_length=20, default='published')
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'article_id': self.id})

    class Meta:
        verbose_name = '博文'
        verbose_name_plural = verbose_name

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


class Category(models.Model):

    name = models.CharField(max_length=100, default='', verbose_name="分类名称")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class ArticleUser(models.Model):
    support_choice = (
        (1, '顶'),
        (0, '踩'),
    )

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    support = models.IntegerField(choices=support_choice, default=None, blank=True, null=True)
    comment = models.TextField(verbose_name='评论', default=None, null=True)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    collect = models.BooleanField(db_column='collect', default=False, verbose_name='收藏')
    blog_times = models.IntegerField(verbose_name='诵经次数', default=0, blank=True, null=True)

    class Meta:
        verbose_name = '支持对应用户的中间表'
        verbose_name_plural = verbose_name
        db_table = "article_user_relationship"
        # unique_together = (("article", "user"),)  # 设置联合主键
        # permissions = (
        #     ('port_vuls_list', u'资产对应漏洞信息中间表'),
        # )


# 访问网站的ip地址和次数
class UserIp(models.Model):
    ip = models.CharField(verbose_name='IP地址', max_length=35)
    count = models.IntegerField(verbose_name='访问次数', default=0)  # 该ip访问次数

    class Meta:
        verbose_name = '访问用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


class VisitNumber(models.Model):
    count = models.IntegerField(verbose_name='网站访问总次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站访问总次数'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.count)


# 单日访问量统计
class DayNumber(models.Model):
    day = models.DateField(verbose_name='日期', default=timezone.now)
    count = models.IntegerField(verbose_name='网站访问次数', default=0)  # 网站访问总次数

    class Meta:
        verbose_name = '网站日访问量统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.day)


class MeritTo(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=20, default='')
    age = models.IntegerField(verbose_name='年龄', default=0)
    content = models.TextField(verbose_name='内容', default='')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default='')


class Wiki(models.Model):
    name = models.CharField(verbose_name='名称', max_length=255, default='')
    content = models.TextField(verbose_name='内容', default='')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    views = models.PositiveIntegerField('浏览量', default=0)

    class Meta:
        verbose_name = 'wiki'
        verbose_name_plural = verbose_name

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


class Excerpt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    content = models.TextField(verbose_name='内容', default='')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    article_id = models.IntegerField(default=0)

    class Meta:
        verbose_name = '摘抄'
        verbose_name_plural = verbose_name


class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    s_content = models.TextField(verbose_name='源内容', default='')
    i_content = models.TextField(verbose_name='想法内容', default='')

    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    article_id = models.IntegerField(default=0)

    class Meta:
        verbose_name = '批注'
        verbose_name_plural = verbose_name
