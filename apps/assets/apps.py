from django.apps import AppConfig
import os


class AssetsConfig(AppConfig):
    name = 'apps.' + os.path.split(os.path.dirname(__file__))[-1]
    verbose_name = '资产'
