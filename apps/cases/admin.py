from django.contrib import admin
from . import models


@admin.register(models.CaseField)
class CaseFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'm_time']
    readonly_fields = ['m_time']


@admin.register(models.Vul)
class VulAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level', 'm_time']
    search_fields = ('name',)
    readonly_fields = ['m_time']


@admin.register(models.Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'case_field', 'vul', 'type', 'function_point', 'm_time']
    search_fields = ('vul', 'function_point',)
    list_display_links = ['vul']
    readonly_fields = ['m_time']


@admin.register(models.FunctionPoint)
class FunctionPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'm_time']
    filter_horizontal = ('vuls',)

    search_fields = ('name', 'vuls',)
    list_display_links = ['name']
    readonly_fields = ['m_time']