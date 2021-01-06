from django.apps import AppConfig
import os


class WebAPPsConfig(AppConfig):
    name = 'apps.' + os.path.split(os.path.dirname(__file__))[-1]
    verbose_name = 'WEB系统'
