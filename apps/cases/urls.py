from . import views
from django.urls import path

app_name = 'cases'

urlpatterns = [
    path('', views.cases_index, name="cases_index"),
    path('search', views.cases_search, name="cases_search"),
    path('<str:field>/<str:vul>/<str:function>', views.case_detail, name="case_detail"),

]
