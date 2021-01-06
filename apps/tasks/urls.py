from . import views
from django.urls import path

app_name = 'tasks'
urlpatterns = [
    path('<int:id>/start', views.task_action, name='task_action'),
]
