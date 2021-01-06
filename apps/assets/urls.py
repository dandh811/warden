from apps.assets import views
from django.urls import path

app_name = 'assets'

urlpatterns = [
    path('risk/comment/post', views.risk_comment_post, name="risk_comment_post"),
]