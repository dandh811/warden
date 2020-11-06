from django.contrib import admin
from . import models


@admin.register(models.CaseField)
class CaseFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'm_time']
    readonly_fields = ['m_time', 'c_time']


@admin.register(models.Vul)
class VulAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level', 'm_time']
    search_fields = ('name',)
    readonly_fields = ['m_time', 'c_time']


@admin.register(models.Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'case_field', 'vul', 'm_time']
    search_fields = ('name', 'm_time',)
    list_display_links = ['name']
    readonly_fields = ['m_time', 'c_time']
