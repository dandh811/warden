from . import views
from django.urls import path

app_name = 'tools'

urlpatterns = [
    path('', views.tools_index, name="tools_index"),
    path('category/<str:category>', views.tools_category, name="tools_category"),
    path('unicode2zh_p', views.unicode2zh_p, name="unicode2zh_p"),
    path('unicode2zh_n', views.unicode2zh_n, name="unicode2zh_n"),
    path('xss_encoding', views.xss_encoding, name="xss_encoding"),

    # path('unicode2zh', views.unicode2zh, name="unicode2zh"),

]
