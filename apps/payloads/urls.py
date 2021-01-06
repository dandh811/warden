from django.conf.urls import url
from apps.payloads import views

app_name = 'payloads'

urlpatterns = [
    url(r'^list/(?P<page>[0-9]+)', views.payloads_list, name='payloads_list'),  # 资产列表
]