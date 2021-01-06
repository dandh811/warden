from django.contrib import admin
from apps.financial import models


@admin.register(models.Investors)
class InvestorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['-id']


@admin.register(models.Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['platform']
    readonly_fields = ['id']
    list_per_page = 100
    ordering = ['-id']


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    readonly_fields = ['id']
    list_per_page = 100
    ordering = ['-id']


@admin.register(models.Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'platform', 'bank', 'investors', 'year_rate', "start_date", 'end_date', 'loan_days', 'capital', 'completed', 'interest_day', 'interest_total']
    list_filter = ['investors', 'completed']
    search_fields = ['platform', 'desc']
    readonly_fields = ['id', 'interest_day', 'interest_total', 'loan_days']
    list_per_page = 100
    ordering = ['completed', 'end_date']
    list_editable = ['completed']
    list_display_links = ['id', 'platform']
