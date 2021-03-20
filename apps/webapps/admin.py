from django.contrib import admin
from . import models


@admin.register(models.WebApp)
class WebAPPAdmin(admin.ModelAdmin):
    list_display = ['id', 'subdomain', 'in_scope', 'status_code', 'server', 'platform', 'm_time']
    search_fields = ('subdomain', 'ip', 'server', 'status_code')
    readonly_fields = ['status_code', 'm_time', 'server', 'ip', 'port', 'other_info']
    list_filter = ['status_code']
    list_editable = ['in_scope']

    def platform(self, obj):
        domain = models.Domain.objects.get(domain=obj.domain)
        return domain.platform


@admin.register(models.Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'in_scope', 'company', 'subdomains_total', 'platform', 'm_time']
    search_fields = ('domain', 'company', 'platform')
    readonly_fields = ['m_time', 'subdomains_total']
    list_editable = ['in_scope']
    list_filter = ['in_scope']


@admin.register(models.WebUrls)
class UrlAdmin(admin.ModelAdmin):
    list_display = ['url', 'm_time']
    search_fields = ('url',)
    readonly_fields = ['url', 'scanned', 'm_time', 'webapp']
