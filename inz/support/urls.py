from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^add_support_ticket', views.add_SupportTicket, name='add-support-ticket'),
    re_path(r'^list_tickets', views.listTickets, name='list-tickets'),
    re_path(r'^show_ticket/(?P<ticket_id>\d+)', views.showTicket, name='show-ticket'),
    re_path(r'^add_comment/(?P<ticket_id>\d+)$', views.add_comment, name='add-comment'),
    re_path(r'^list_support_tickets/', views.list_support_tickets, name='list-support-tickets'),
    re_path(r'^update_ticket/(?P<ticket_id>\d+)', views.update_ticket, name='update-ticket'),
]
