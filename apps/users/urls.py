from django.conf.urls import url, include
from apps.users import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    url(r'^register$', views.register, name='register'),
    path('email/check', views.email_check, name='email_check'),
    path('nickname/check', views.nickname_check, name='nickname_check'),
    path('confirm/', views.user_confirm),
    path('wechat/login', views.wechat_login, name='wechat_login'),

    url(r'^login$', views.login_site, name='login'),
    url(r'^findpass$', views.find_pass, name='find_pass'),
    url(r'^captcha', include('captcha.urls')),
    url(r'captcha/refresh/$', views.captcha_refresh, name='captcha_refresh'),
    url(r'^logout$', views.logout_site, name='logout'),
    url(r'^center$', views.user_center, name='user_center'),
    url(r'^set$', views.user_set, name='user_set'),
    url(r'^u/(?P<user_id>[0-9]+)$', views.user_home, name='user_home'),
    url(r'^update/info$', views.update_user_info, name='update_user_info'),
    url(r'^manage/user/disactivate/$', views.user_disactivate, name='userdisactivate'),
    url(r'^manage/userrequest/stop/$', views.user_request_cancle, name='userregiststop'),
    url(r'^img/upload$', views.upload_image, name='img_upload'),
]
