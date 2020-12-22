from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from markdown import markdown
from django.utils.html import mark_safe
from django.utils.html import format_html


class Category(models.Model):

    name = models.CharField(max_length=100, default='', verbose_name="分类名称")
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    icon = models.CharField(max_length=30, default='fa-home',verbose_name='菜单图标')

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
    type_choice = (
        ('share', '分享'),
        ('help', '求助'),
        ('advice', '建议'),
        ('notice', '公告'),

    )

    status_choice = (
        ('draft', '草稿'),
        ('published', '发布'),
        ('recycle', '回收站'),
        ('private', '私有'),

    )
    title = models.CharField(max_length=100, default='', verbose_name="名称")
    category = models.ForeignKey(Category, verbose_name='分类', max_length=20, default='', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    support = models.IntegerField(default=0, verbose_name='点赞数', null=True, blank=True)
    content = models.TextField('内容', default='', blank=True, null=True)
    status = models.CharField(choices=status_choice, null=True, blank=True, verbose_name='状态', max_length=20, default='published')
    views = models.PositiveIntegerField('浏览量', default=0)
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    cover = models.CharField(max_length=200, default='https://image.3001.net/images/20200304/15832956271308.jpg', verbose_name='文章封面')
    desc = models.TextField(max_length=150, verbose_name='文章描述', default='')

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

    # def get_message_as_markdown(self):
    #     return mark_safe(markdown(self.content, safe_mode='escape'))


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


class Site(models.Model):
    """
    站点配置
    """
    desc = models.CharField(max_length=50, verbose_name='网站描述')
    keywords = models.CharField(max_length=50, verbose_name='网站关键词')
    title = models.CharField(max_length=50, verbose_name='网站标题')
    index_title = models.CharField(max_length=50, verbose_name='首页标题')
    type_chinese = models.CharField(max_length=50, verbose_name='座右铭汉语')
    type_english = models.CharField(max_length=80, verbose_name='座右铭英语')
    icp_number = models.CharField(max_length=20, verbose_name='备案号')
    icp_url = models.CharField(max_length=50, verbose_name='备案链接')
    site_mail = models.CharField(max_length=50, verbose_name='我的邮箱')
    site_qq = models.CharField(max_length=50, verbose_name='我的QQ')
    site_avatar = models.CharField(max_length=200, default='https://himg.bdimg.com/sys/portrait/item/pp.1.102d4e0b.kcf3RFn3qxXFsjWSxZam_Q.jpg', verbose_name='我的头像')

    class Meta:
        verbose_name = '网站设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
