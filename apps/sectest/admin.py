from django.contrib import admin
from apps.sectest import models


@admin.register(models.XssPrey)
class XssPreyAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'user_agent', 'cookie', 'ip']
    ordering = ['-id']


@admin.register(models.PackagePrey)
class PackagePreyAdmin(admin.ModelAdmin):
    list_display = ['msg', 'm_time']
    readonly_fields = ['msg', 'm_time']
    search_fields = ['msg']
