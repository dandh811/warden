from django.urls import path
from . import views

app_name = 'financial2'

urlpatterns = [
    path('wxlogin', views.wxlogin, name="wxlogin"),
    path('get/investment', views.get_investment, name="get_investment"),
    path('get/statistical', views.get_statistical, name="get_statistical"),
    # path('category/<str:category>', views.articles_category, name="articles_category"),
    path('new', views.new, name="new"),
    # path('support', views.article_support, name="article_support"),
    # path('add_blog_times', views.add_blog_times, name="add_blog_times"),
    # path('search', views.article_search, name="article_search"),
    # path('about', views.about, name="about"),
    # path('tag/<str:tag>', views.articles_tag, name="articles_tag"),

]
