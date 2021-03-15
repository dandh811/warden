from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from mdeditor.fields import MDTextField


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')

    # 统计文章数 并放入后台
    def get_items(self):
        return len(self.article_set.all())

    get_items.short_description = '文章数'

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=100, default='', verbose_name="分类名称")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    icon = models.CharField(max_length=30, default='fa-home',verbose_name='菜单图标')
    active = models.BooleanField(default=True, verbose_name='是否添加到菜单')

    def get_items(self):
        return len(self.article_set.all())

    def icon_data(self):
        return format_html(
            '<i class="{}"></i>',
            self.icon,
        )

    get_items.short_description = '文章数'
    icon_data.short_description = '图标预览'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Article(models.Model):

    status_choice = (
        ('draft', '草稿'),
        ('published', '发布'),
        ('recycle', '回收站'),
        ('private', '私有'),

    )
    title = models.CharField(max_length=100, default='', verbose_name="名称")
    category = models.ForeignKey(Category, verbose_name='分类', max_length=20, default='', on_delete=models.CASCADE)
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    support = models.IntegerField(default=0, verbose_name='点赞数', null=True, blank=True)
    content = MDTextField('内容', default='', blank=True, null=True)
    status = models.CharField(choices=status_choice, null=True, blank=True, verbose_name='状态', max_length=20, default='published')
    views = models.PositiveIntegerField('浏览量', default=0)
    desc = models.TextField(max_length=150, verbose_name='文章描述', default='')
    tag = models.ManyToManyField(Tag, verbose_name='文章标签', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:article_detail', kwargs={'title': self.title})

    class Meta:
        verbose_name = '博文'
        verbose_name_plural = verbose_name

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


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
    blog_times = models.IntegerField(verbose_name='次数', default=0, blank=True, null=True)

    class Meta:
        verbose_name = '支持对应用户的中间表'
        verbose_name_plural = verbose_name
        db_table = "article_user_relationship"


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
