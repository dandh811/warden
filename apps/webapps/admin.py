from django.contrib import admin
from . import models


@admin.register(models.WebApp)
class WebAPPAdmin(admin.ModelAdmin):
    list_display = ['subdomain', 'status_code', 'ip', 'platform', 'manual', 'm_time']
    search_fields = ('subdomain', 'ip', 'server', 'status_code')
    readonly_fields = ['status_code', 'm_time', 'server', 'ip', 'port', 'other_info']
    list_filter = ['status_code']

    def platform(self, obj):
        domain = models.Domain.objects.get(domain=obj.domain)
        return domain.platform


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'company', 'subdomains_total', 'platform', 'm_time']
    search_fields = ('domain', 'company', 'm_time', 'platform')
    readonly_fields = ['m_time', 'subdomains_total']


@admin.register(models.WebUrls)
class UrlAdmin(admin.ModelAdmin):
    list_display = ['url', 'm_time']
    search_fields = ('url', 'm_time')