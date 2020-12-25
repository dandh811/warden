from django.contrib import admin
from .models import Article, Category, Tag
from django.forms import TextInput, Textarea
from django.db import models
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'c_time', 'cover_data']
    list_filter = ['category', 'status', 'tag']
    search_fields = ('title', 'desc', 'content')
    readonly_fields = ['support', 'c_time', 'views']
    list_editable = ['category', 'status']

    fieldsets = (
        ('编辑文章', {
            'fields': ('title', 'content')
        }),
        ('其他设置', {
            'classes': ('collapse',),
            'fields': ('cover', 'desc', 'is_recommend', 'tag', 'category', 'c_time'),
        }),
    )

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '59'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 59})},
    }


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