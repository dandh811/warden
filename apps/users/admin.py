from . import models
from django.contrib import admin
from django.contrib.auth.models import User


admin.site.unregister(User)  # 去掉在admin中的注册
