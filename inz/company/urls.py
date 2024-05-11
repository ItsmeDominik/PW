from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^list_companies', views.list_companies, name='list-companies'),
    re_path(r'^add_company', views.add_company, name='add-company'),
    re_path(r'^show_company/(?P<company_id>\d+)', views.show_company, name='show-company'),
    ]

