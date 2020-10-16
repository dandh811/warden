from django.contrib import admin
from .models import Article, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'c_time']
    list_filter = ['category', 'status']
    search_fields = ('title', 'category',)
    readonly_fields = ['support', 'c_time', 'views']
    list_editable = ['category', 'status']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'c_time']
    list_filter = ['name', 'c_time']
    search_fields = ('name', 'c_time',)
