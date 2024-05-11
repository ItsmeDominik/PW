from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^add_product', views.add_product, name='add-product'),
    re_path(r'^add_order', views.add_order, name='add-order'),
    re_path(r'^list_products/', views.list_products, name='list-products'),
    re_path(r'^my_orders/', views.user_orders, name='user-orders'),
    re_path(r'^update_order_status/', views.update_order_status, name='update-order-status'),
    re_path(r'^change_order_status/(?P<order_id>\d+)$', views.change_order_status, name='change-order-status'),

]
