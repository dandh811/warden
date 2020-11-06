from django.apps import AppConfig
import os


class CasesConfig(AppConfig):
    name = 'apps.' + os.path.split(os.path.dirname(__file__))[-1]
    verbose_name = '测试用例'
