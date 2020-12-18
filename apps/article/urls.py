from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('', views.index, name="index"),
    path('articles/<str:category>', views.articles_category, name="articles_category"),
    path('article/<str:title>', views.article_detail, name="article_detail"),

    path('comment', views.article_comment, name="article_comment"),
    path('type/<str:type>', views.article_type, name="article_type"),
    path('category/<str:category>', views.articles_category, name="articles_category"),
    path('add/message', views.add_message, name="add_message"),
    path('support', views.article_support, name="article_support"),
    path('collect', views.article_collect, name="article_collect"),
    path('collected', views.article_collected, name="article_collected"),
    path('add_blog_times', views.add_blog_times, name="add_blog_times"),
    path('search', views.article_search, name="article_search"),
    path('about', views.about, name="about"),
]
