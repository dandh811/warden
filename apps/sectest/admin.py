from django.contrib import admin
from apps.sectest import models


@admin.register(models.XssPrey)
class XssPreyAdmin(admin.ModelAdmin):
    list_display = ['id', 'domain', 'user_agent', 'cookie']
    ordering = ['-id']
