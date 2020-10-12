from apps.article.models import Article, ArticleUser
from apps.users.models import User, Profile
from django.db.models import Count


def add_variable_to_context(request):
    # vm = VisitNumber.objects.first()

    # hot_articles = ArticleUser.objects.filter(article__category='scripture').values('article_id').annotate(num_articles=Count('article_id')).order_by('-num_articles')[:10]
    # hot_articles = Article.objects.filter(category='scripture').order_by('-views')[:10]
    # for hk in hot_articles:
    #     try:
    #         hk['title'] = Article.objects.get(id=hk['article_id']).title
    #     except Exception as e:
    #         logger.critical(e)

    # zan_articles = ArticleUser.objects.values('article_id').annotate(num_articles=Count('article_id')).order_by('-num_articles')[:10]
    # for hk in hot_articles:
    #     try:
    #         hk['title'] = Article.objects.get(id=hk['article_id']).title
    #     except Exception as e:
    #         logger.critical(e)

    # hot_users = Profile.objects.order_by('-point')[:10]
    # for hu in hot_users:
    #     try:
    #         hu.username = User.objects.get(id=hu.user_id).username
            # hu['avatar'] = Profile.objects.get(user_id=hu['user_id']).avatar
        # except Exception as e:
        #     logger.critical(e)

    # users = Profile.objects.all()
    # scriptures = Article.objects.filter(category='scripture')
    # musices = Article.objects.filter(category='music')
    # comments = ArticleUser.objects.filter(comment__isnull=True)
    # supports = ArticleUser.objects.filter(support__isnull=True)
    # visitnum = VisitNumber.objects.all()[0].count
# hot_users = articleUser.objects.values('user_id').annotate(num_comments=Count('user_id')).order_by('-num_comments')[:10]
    # for hu in hot_users:
    #     try:
    #         hu['username'] = User.objects.get(id=hu['user_id']).username
    #         hu['avatar'] = Profile.objects.get(user_id=hu['user_id']).avatar
    #     except Exception as e:
    #         logger.critical(e)

    return locals()
