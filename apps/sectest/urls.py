from django.conf.urls import url
from apps.sectest import views
from django.urls import path

app_name = 'sectest'

urlpatterns = [
    url(r'^$', views.exploit_list, name='exploit_list'),
    url(r'^url_illegal_redirect/(?P<paras>.*)$', views.url_illegal_redirect, name='url_illegal_redirect'),
    url(r'^postmessage/attack$', views.postmessage, name='postmessage'),
    path('postmessage/child', views.postmessage_child, name='postmessage_child'),
    path('xss', views.xss, name='xss'),
    path('xss_prey/', views.xss_prey, name='xss_prey'),
    path('xss/test.js', views.xss_js, name='xss_js'),

]