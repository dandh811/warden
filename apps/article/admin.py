from django.contrib import admin
from .models import Article, Category, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'c_time']
    list_filter = ['category', 'status']
    search_fields = ('title',)
    readonly_fields = ['support', 'c_time', 'views']
    list_editable = ['category', 'status']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'c_time']
    list_filter = ['name', 'c_time']
    search_fields = ('name', 'c_time',)


# 标签
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_items')
    search_fields = ('name', )
    readonly_fields = ('get_items',)
    list_per_page = 20