from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from utils.visit_info import update_access_nums
from django.core.paginator import Paginator
from apps.users.models import Profile
from apps.article.models import *
import random
from django.db.models import Q
from loguru import logger


@csrf_exempt
def index(request):
    update_access_nums(request)
    if request.user.is_superuser:
        articles = Article.objects.order_by('-id')
    else:
        articles = Article.objects.filter(status='published').order_by('-id')
    types = Article.type_choice
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    particles = paginator.get_page(page)
    for article in particles:
        article.content = markdown(article.content,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])

    return render(request, 'moments/index.html', locals())


@csrf_exempt
def articles_category(request, category):
    articles = Article.objects.filter(category__name=category, status='published')
    types = Article.type_choice
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    particles = paginator.get_page(page)

    return render(request, 'moments/index.html', locals())


@csrf_exempt
def article_detail(request, title):
    try:
        if request.user.is_superuser:
            article = Article.objects.get(title=title)
        else:
            article = Article.objects.get(Q(title=title) & Q(status='published'))
        blog_times = ArticleUser.objects.filter()
        article.viewed()
        article.content = markdown(article.content,
                                   extensions=[
                                       'markdown.extensions.extra',
                                       'markdown.extensions.codehilite',
                                       'markdown.extensions.toc',
                                   ])
        comments = ArticleUser.objects.filter(article__title=title).exclude(comment=None)
        return render(request, 'moments/article.html', locals())
    except Exception as e:
        logger.critical(e)


def article_type(request, type):
    ks = Article.objects.filter(type=type)
    types = Article.type_choice
    paginator = Paginator(ks, 15)
    page = request.GET.get('page')
    pks = paginator.get_page(page)

    return render(request, 'moments/index.html', locals())


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
@login_required
def article_collect(request):
    # types = models.article.type_choice
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Exception as e:
        logger.critical(e)
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        action = request.POST.get('action')
        if action == 'collect':
            try:
                ArticleUser.objects.update_or_create(article_id=article_id, user_id=request.user.id, defaults={'collect': True})
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                logger.critical(e)
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            try:
                ArticleUser.objects.update_or_create(article_id=article_id, user_id=request.user.id, defaults={'collect': False})
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                logger.critical(e)
                return HttpResponse('{"status":"fail"}', content_type='application/json')
    else:
        return render(request, 'article/article_detail.html', locals())


@csrf_exempt
def article_collected(request):
    # articles = ArticleUser.objects.filter(Q(user=request.user) | Q(collect=1))
    articles = Article.objects.filter(Q(articleuser__collect=1) | Q(articleuser__user=request.user))
    paginator = Paginator(articles, 15)
    page = request.GET.get('page')
    particles = paginator.get_page(page)

    return render(request, 'moments/index.html', locals())


@csrf_exempt
def article_search(request):
    q = request.GET.get('q')
    if request.user.is_superuser:
        ks = Article.objects.filter(title__icontains=q)
    else:
        ks = Article.objects.filter(Q(title__icontains=q) & Q(status='published'))

    paginator = Paginator(ks, 15)
    page = request.GET.get('page')
    particles = paginator.get_page(page)

    return render(request, 'moments/index.html', locals())


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
@login_required
def add_idea(request):
    if request.method == 'POST':
        try:
            article_id = request.POST['article_id']
            i_content = request.POST['i_content']

            content = request.POST.get('content')
            if not content:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
            else:
                Idea.objects.update_or_create(article_id=article_id, s_content=content, user=request.user, i_content=i_content)
                return HttpResponse('{"status":"success"}', content_type='application/json')
        except Exception as e:
            logger.critical(e)
            return HttpResponse('{"status":"fail"}', content_type='application/json')
