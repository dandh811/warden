from django.conf.urls import url
from apps.users import views

app_name = 'users'

urlpatterns = [
    url(r'^logout$', views.logout_site, name='logout'),
    url(r'^manage/user/disactivate/$', views.user_disactivate, name='userdisactivate'),
    url(r'^manage/userrequest/stop/$', views.user_request_cancle, name='userregiststop'),
]
