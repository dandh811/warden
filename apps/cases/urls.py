from . import views
from django.urls import path

app_name = 'cases'

urlpatterns = [
    path('', views.cases_index, name="cases_index"),
    path('search', views.cases_search, name="cases_search"),

]
