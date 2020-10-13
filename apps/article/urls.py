from django.urls import path, re_path
from . import views

app_name = 'article'

urlpatterns = [
    path('', views.index, name="index"),
    path('merit_to', views.merit_to_index, name="merit_to_index"),
    path('wikis', views.wikis, name="wikis"),
    path('wiki/<int:wiki_id>', views.wiki_detail, name="wiki_detail"),

    path('articles/<str:category>', views.articles_category, name="articles_category"),

    path('article/<int:article_id>', views.article_detail, name="article_detail"),

    path('comment', views.article_comment, name="article_comment"),
    path('type/<str:type>', views.article_type, name="article_type"),
    path('category/<int:category_id>', views.articles_category, name="articles_category"),
    path('add/message', views.add_message, name="add_message"),
    path('add/excerpt', views.add_excerpt, name="add_excerpt"),
    path('add/idea', views.add_idea, name="add_idea"),

    path('support', views.article_support, name="article_support"),
    path('collect', views.article_collect, name="article_collect"),
    path('collected', views.article_collected, name="article_collected"),
    path('add_blog_times', views.add_blog_times, name="add_blog_times"),
    path('add_merit_to', views.add_merit_to, name="add_merit_to"),
    path('search', views.article_search, name="article_search"),
    path('about', views.about, name="about"),
]
