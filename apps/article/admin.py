from django.contrib import admin
from .models import Article, Category, Wiki


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'c_time']
    list_filter = ['title', 'category']
    search_fields = ('title', 'category',)
    readonly_fields = ['support', 'c_time', 'views']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'c_time']
    list_filter = ['name', 'c_time']
    search_fields = ('name', 'c_time',)


@admin.register(Wiki)
class WikiAdmin(admin.ModelAdmin):
    list_display = ['name', 'c_time']
    list_filter = ['name', 'c_time']
    search_fields = ('name', 'c_time',)
