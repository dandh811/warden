from __future__ import unicode_literals

from django.apps import AppConfig
import os


class ToolkitConfig(AppConfig):
    name = 'apps.' + os.path.split(os.path.dirname(__file__))[-1]
    verbose_name = '工具箱'
