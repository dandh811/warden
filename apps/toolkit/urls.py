from .views import *
from django.urls import path

app_name = 'toolkit'

urlpatterns = [
    path('index', index, name='index'),
    path('json_xml', json_xml, name='json_xml'),
    path('base64', base64_handle, name='base64'),
    path('whathash', whathash, name='whathash'),
    path('whois', whois_handle, name='whois'),
    path('xss', xss, name='xss'),
    path('smuggler', smuggler, name='smuggler'),
    path('FindSubdomains', find_subdomains, name='find_subdomains'),

]
