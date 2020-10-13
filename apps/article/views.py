from django.shortcuts import render
from django.http import HttpResponse
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
    articles = Article.objects.filter(status='published')
    types = Article.type_choice
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    particles = paginator.get_page(page)
    for p in particles:
        if p.cover:
            p.article_image_url = p.cover
        else:
            p.article_image_url = '/media/article_images/%s.jpg' % (random.randint(0, 25))

    return render(request, 'article/article_index.html', locals())


@csrf_exempt
def articles_category(request, category):
    articles = Article.objects.filter(category=category, status='published')
    types = Article.type_choice
    paginator = Paginator(articles, 10)
    page = request.GET.get('page')
    particles = paginator.get_page(page)
    for p in particles:
        if p.cover:
            p.article_image_url = p.cover
        else:
            p.article_image_url = '/media/article_images/%s.jpg' % (random.randint(0, 25))

    return render(request, 'article/article_index.html', locals())


@csrf_exempt
def article_detail(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        blog_times = ArticleUser.objects.filter()
        article.viewed()

        comments = ArticleUser.objects.filter(article_id=article_id).exclude(comment=None)
        if article.category == 'music':
            return render(request, 'article/music_detail.html', locals())
        else:
            return render(request, 'article/article_detail.html', locals())
    except Exception as e:
        logger.critical(e)


@csrf_exempt
def wikis(request):
    wikis = Wiki.objects.all()
    blog_times = ArticleUser.objects.filter()

    return render(request, 'article/wikis_list.html', locals())


@csrf_exempt
def wiki_detail(request, wiki_id):
    wiki = Wiki.objects.get(id=wiki_id)
    wiki.viewed()

    return render(request, 'article/wiki_detail.html', locals())


def article_type(request, type):
    ks = Article.objects.filter(type=type)
    types = Article.type_choice
    paginator = Paginator(ks, 15)
    page = request.GET.get('page')
    pks = paginator.get_page(page)

    return render(request, 'article/article_index.html', locals())


@csrf_exempt
def article_comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        article_id = request.POST.get('article_id')

        try:
            user_profile = Profile.objects.get(user=request.user)
            try:
                ArticleUser.objects.update_or_create(article_id=article_id, user=request.user, defaults={'comment': content})
                user_profile.point = int(user_profile.point) + 1
                user_profile.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            except Exception as e:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
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

    return render(request, 'article/article_index.html', locals())


@csrf_exempt
def article_search(request):
    q = request.POST.get('q')
    ks = Article.objects.filter(title__icontains=q)
    paginator = Paginator(ks, 15)
    page = request.GET.get('page')
    particles = paginator.get_page(page)
    for p in particles:
        if p.cover:
            p.article_image_url = p.cover
        else:
            p.article_image_url = '/media/article_images/%s.jpg' % (random.randint(0, 20))

    return render(request, 'article/article_index.html', locals())


# def category(request, pk):
#     """
#     :param request:
#     :param pk:
#     :return:
#     相应分类下的窍门检索
#     """
#     try:
#         cate = Category.objects.get(pk=pk)
#     except Category.DoesNotExist:  # 读取分类，如果不存在，则引发错误，并404
#         raise Http404
#
#     ks = cate.c.all()  ## 获取分类下的所有文章
#     # return render_to_response('blog/index.html', ## 使用首页的文章列表模版，但加入了的一个`is_category`开关
#     #     {"posts": posts,
#     #     "is_category": True,
#     #     "cate_name": cate.name,
#     #     "categories": Category.objects.all()},
#     # context_instance=RequestContext(request))


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
def add_merit_to(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        content = request.POST.get('content')
        article_id = request.POST.get('article_id')
        try:
            MeritTo.objects.create(name=name, age=age, content=content, article_id=article_id)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        except Exception as e:
            logger.critical(e)
            return HttpResponse('{"status":"fail"}', content_type='application/json')


@csrf_exempt
def merit_to_index(request):
    all_mts = MeritTo.objects.order_by('-id')
    paginator = Paginator(all_mts, 15)
    page = request.GET.get('page')
    mts = paginator.get_page(page)

    return render(request, 'article/merit_to_index.html', locals())


@csrf_exempt
@login_required
def add_excerpt(request):
    """摘录"""
    if request.method == 'POST':

        try:
            article_id = request.POST['article_id']
            content = request.POST.get('content')
            if not content:
                return HttpResponse('{"status":"fail"}', content_type='application/json')
            else:
                Excerpt.objects.update_or_create(article_id=article_id, content=content, user=request.user)
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
