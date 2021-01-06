from django.contrib import admin
from apps.tasks.models import Task, Plugins
from django.utils.html import format_html


@admin.register(Plugins)
class PluginsAdmin(admin.ModelAdmin):
    list_display = ['name', 'verbose_name', 'tick_status', 'm_time']
    search_fields = ['name']
    readonly_fields = ['m_time']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    filter_horizontal = ('plugins',)
    search_fields = ['name']

    def buttons(self, obj):
        return format_html('<a style="color: red" href="/task/{}/start">开始任务</a> ', obj.id)

    buttons.short_description = "操作"
    list_display = ['name', 'buttons', 'type', 'policy', 'target', 'm_time']
    ordering = ['name']
