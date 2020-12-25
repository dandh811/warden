from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from utils.visit_info import update_access_nums
from django.core.paginator import Paginator
from apps.users.models import Profile
from apps.article.models import *
from django.db.models import Q
from loguru import logger
from django.conf import settings
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import mistune
import random
from django.views.generic.base import View
from urllib.parse import unquote


def global_setting(request):
    """
    将settings里面的变量 注册为全局变量
    """
    active_categories = Category.objects.all()
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_DESC': settings.SITE_DESCRIPTION,
        'SITE_KEY': settings.SECRET_KEY,
        'SITE_MAIL': settings.SITE_MAIL,
        'SITE_ICP': settings.SITE_ICP,
        'SITE_ICP_URL': settings.SITE_ICP_URL,
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_TYPE_CHINESE': settings.SITE_TYPE_CHINESE,
        'SITE_TYPE_ENGLISH': settings.SITE_TYPE_ENGLISH,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'active_categories': active_categories
    }


@csrf_exempt
def index(request):
    update_access_nums(request)
    if request.user.is_superuser:
        articles = Article.objects.order_by('-id')
    else:
        articles = Article.objects.filter(status='published').order_by('-id')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    for article in articles:
        article.cover = 'http://www.dongjianjun.com/static/images/covers/%s.jpg' % random.randint(0,20)

    # paginator = Paginator(articles, 10)
    # page = request.GET.get('page')
    # particles = paginator.get_page(page)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(articles, 9, request=request)
    articles = p.page(page)


    # for article in particles:
    #     article.content = markdown.markdown(article.content,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                               ])

    return render(request, 'hexo/index.html', locals())


@csrf_exempt
def articles_category(request, category):
    articles = Article.objects.filter(category__name=category, status='published')
    for article in articles:
        article.cover = 'http://www.dongjianjun.com/static/images/covers/%s.jpg' % random.randint(0,20)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(articles, 9, request=request)
    articles = p.page(page)

    return render(request, 'hexo/index.html', locals())


@csrf_exempt
def article_detail(request, title):
    try:
        if request.user.is_superuser:
            article = Article.objects.get(title=title)
        else:
            article = Article.objects.get(Q(title=title) & Q(status='published'))
        # blog_times = ArticleUser.objects.filter()
        article_url = unquote(article.get_absolute_url(), 'utf-8')
        article.viewed()
        mk = mistune.Markdown()
        output = mk(article.content)
        # md = markdown.Markdown(
        #     extensions=[
        #         'markdown.extensions.extra',
        #         'markdown.extensions.codehilite',
        #         'markdown.extensions.toc',
        #     ]
        # )
        # article.content = md.convert(article.content)

        # context = {'article': article, 'toc': md.toc}

        # comments = ArticleUser.objects.filter(article__title=title).exclude(comment=None)
        return render(request, 'hexo/detail.html', locals())
    except Exception as e:
        logger.critical(e)


@csrf_exempt
def article_comment(request):
    """
    文章评论
    """
    if request.method == 'POST':
        content = request.POST.get('content')
        article_id = request.POST.get('article_id')
        article = Article.objects.get(id=article_id)
        try:
            user_profile = Profile.objects.get(user=request.user)
            ArticleUser.objects.update_or_create(article_id=article_id, user=request.user, defaults={'comment': content})
            user_profile.point = int(user_profile.point) + 1
            user_profile.save()
            # return HttpResponse('{"status":"success"}', content_type='application/json')
            return HttpResponseRedirect(reverse('article:article_detail', args=[article.title]))
        except Exception as e:
            logger.critical(e)


@csrf_exempt
def add_message(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')

            try:
                Article.objects.create(title=title, content=content, category='message')
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                logger.critical(e)
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            return render(request, 'article/add_message.html', locals())
    except Exception as e:
        logger.critical(e)


@csrf_exempt
@login_required
def article_support(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        action = request.POST.get('action')
        article = Article.objects.get(id=article_id)
        if action == 'support':
            try:
                article.support = int(article.support) + 1
                article.save()
                ArticleUser.objects.update_or_create(article_id=article_id, user=request.user, defaults={'support': 1})
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                logger.critical(e)
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            try:
                article.support = int(article.support) - 1
                article.save()
                ArticleUser.objects.update_or_create(article_id=article_id, user=request.user, defaults={'support': 0})
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                logger.critical(e)
                return HttpResponse('{"status":"fail"}', content_type='application/json')
    else:
        return render(request, 'article/article_detail.html', locals())


@csrf_exempt
def article_search(request):
    if request.user.is_superuser:
        articles = Article.objects.all()
    else:
        articles = Article.objects.filter(status='published')
    entries = []
    for article in articles:
        article_url = unquote(article.get_absolute_url(), 'utf-8')
        entry = '<entry><title>%s</title><link href="%s"/><url>%s</url><categories><category> %s </category></categories></entry>' % \
                (article.title, article_url, article_url, article.category)
        entries.append(entry)
    datas = '<?xml version="1.0" encoding="utf-8"?><search>' + ''.join(entries) + '</search>'
    return HttpResponse(datas, content_type="text/xml")


@csrf_exempt
def about(request):

    return render(request, 'article/about.html', locals())


@csrf_exempt
@login_required
def add_blog_times(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        try:
            cur_blog_times = ArticleUser.objects.get(Q(article_id=article_id) & Q(user=request.user)).blog_times
        except Exception as e:
            cur_blog_times = 0
            logger.critical(e)
        new_blog_times = cur_blog_times + 1
        try:
            ArticleUser.objects.update_or_create(article_id=article_id, user_id=request.user.id, defaults={'blog_times': new_blog_times})
            return HttpResponse('{"status":"success"}', content_type='application/json')
        except Exception as e:
            logger.critical(e)
            return HttpResponse('{"status":"fail"}', content_type='application/json')


@csrf_exempt
def articles_tag(request, tag):
    tags = Tag.objects.all()
    articles = Article.objects.filter(tag__name=tag, status='published')
    for article in articles:
        article.cover = 'http://www.dongjianjun.com/static/images/covers/%s.jpg' % random.randint(0,20)
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1
    p = Paginator(articles, 9, request=request)
    articles = p.page(page)

    return render(request, 'hexo/article_tag.html', locals())
