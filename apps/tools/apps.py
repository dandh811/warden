from django.apps import AppConfig
import os


class ToolsConfig(AppConfig):
    name = 'apps.' + os.path.split(os.path.dirname(__file__))[-1]
    verbose_name = '在线工具'
