from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^add_news', views.add_news, name="add-news"),
    re_path(r'^list_news_update', views.list_news_update, name='list-update-news'),
    re_path(r'^list_news', views.list_news, name="list-news"),
    re_path(r'^show_news/(?P<news_id>\d+)', views.show_news, name='show-news'),
    re_path(r'^update_news/(?P<news_id>\d+)', views.update_news, name='update-news'),
    re_path(r'^delete_news/(?P<news_id>\d+)', views.delete_news, name='delete-news'),


    re_path(r'^add_discount/', views.add_discount, name="add-discount"),
    re_path(r'^list_discount/$', views.list_discount, name="list-discount-default"),
    re_path(r'^list_discount/(?P<company_id>\d+)$', views.list_discount, name="list-discount"),
    re_path(r'^update_discount/(?P<discount_id>\d+)', views.update_discount, name="update-discount"),
    re_path(r'^delete_discount/(?P<discount_id>\d+)', views.delete_discount, name="delete-discount"),
    re_path(r'^show_discount/(?P<discount_id>\d+)', views.show_discount, name="show-discount"),



]
