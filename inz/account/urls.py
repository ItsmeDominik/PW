from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^login_user', views.login_user, name='login-user'),
    re_path(r'^logout_user', views.logout_user, name='logout-user'),
    re_path(r'^register_user', views.register_user, name='register-user'),
    re_path(r'^list_users', views.list_users, name='list-users'),
    re_path(r'^list_company_users/(?P<company_id>\d+)', views.list_company_users, name='list-company-users'),
]