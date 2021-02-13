from django.contrib import admin
from apps.assets import models


@admin.register(models.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['ip', "m_time"]
    search_fields = ('ip',)


@admin.register(models.Risk)
class RiskAdmin(admin.ModelAdmin):
    list_display = ['id', 'risk_type', 'target', 'status', 'bounty']
    list_filter = ['risk_type', 'status']
    search_fields = ['risk_type', 'target', 'desc', 'status']
    readonly_fields = ['target', 'risk_type', 'desc']
    list_per_page = 100
    ordering = ['-id']
    list_editable = ['status']
    fk_fields = ['target']  # 设置显示外键字段，好像没什么用
    list_display_links = ['id', 'risk_type']


@admin.register(models.Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ['nmap_name', 's_num', 'comment']
    actions = ['modify_whitelist']
    readonly_fields = ['nmap_name']
    search_fields = ['nmap_name']

    def s_num(self, obj):
        ports = models.Port.objects.filter(software_name=obj)
        return len(ports)

    s_num.short_description = u"统计数量"


@admin.register(models.Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ['port_num', 'software_name', 'software_version', 'service_name', 'asset', 'm_time']
    readonly_fields = ['asset', 'port_num', 'software_name', 'software_version', 'service_name', 'scanned']
    search_fields = ['port_num', 'software_name', 'service_name']

    def s_num(self, obj):
        ports = models.Port.objects.filter(software_name=obj)
        return len(ports)

    s_num.short_description = u"统计数量"


# @admin.register(models.Bounty)
# class BountyAdmin(admin.ModelAdmin):
#     list_display = ['']
