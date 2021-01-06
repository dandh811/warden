from . import views
from django.urls import path

app_name = 'webapps'

urlpatterns = [
    path('report/<int:webapp_id>', views.webapp_report, name="webapp_report"),

]
