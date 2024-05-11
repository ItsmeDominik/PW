from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^list_rooms_reservation/', views.list_reservation_rooms, name='list-rooms-reservation'),
    re_path(r'^list_office_rooms/', views.list_office_rooms, name='list-offices'),
    re_path(r'^list_rooms/', views.list_rooms, name='list_rooms'),
    re_path(r'^add_room', views.add_room, name='add-room'),
    re_path(r'^add_printer/', views.add_printer, name='add-printer'),
    re_path(r'^update_printer/(?P<printer_id>\d+)', views.update_printer, name='update-printer'),
    re_path(r'^update_printer_status/(?P<printer_id>\d+)', views.update_printer_status, name='update-printer-status'),
    re_path(r'^list_update_printer', views.list_update_printer, name='list-update-printer'),
    re_path(r'^list_rent_printer', views.list_rent_printer, name='list-rent-printer'),
    re_path(r'^list_printers', views.list_printers, name='list-printers'),
    re_path(r'^list_rented_printer', views.list_rented_printer, name='list-rented-printer'),
    re_path(r'^expired_rented_printers/', views.expired_rented_printers, name='expired-rented-printers'),
    re_path(r'^update_printer_status_expired/(?P<printer_id>\d+)', views.update_printer_status_expired, name='update-printer-status-expired'),
    re_path(r'^add_reservation/(?P<room_id>\d+)', views.add_RoomReservation, name='add-reservation'),
    re_path(r'^add_rent/(?P<room_id>\d+)', views.add_OfficeRent, name='add-office-rent'),
    re_path(r'^add_printer_rent/(?P<printer_id>\d+)', views.add_printer_rent, name='add-printer-rent'),
    re_path(r'^show_rooms/(?P<room_id>\d+)', views.show_rooms, name='show-room'),
    re_path(r'^my_reservations/$', views.myReservations, name='my-reservations'),
    re_path(r'^my_rents/$', views.myRents, name='my-rents'),
    re_path(r'^my_printer/$', views.my_printers, name='my-printers'),
    re_path(r'^delete-reservation/(?P<reservation_id>\d+)', views.deleteReservation, name='delete-reservation'),
    re_path(r'^list_update_room', views.list_update_room, name='list-update-room'),
    re_path(r'^list_update_office', views.list_update_office, name='list-update-office'),
    re_path(r'^list_update_conference_room', views.list_update_conference_room, name='list-update-conference-room'),
    re_path(r'^update_rooms/(?P<room_id>\d+)', views.update_room, name='update-room'),
    re_path(r'^delete_room/(?P<room_id>\d+)', views.delete_room, name='delete-room'),
    re_path(r'^delete_printer/(?P<printer_id>\d+)', views.delete_printer, name='delete-printer'),
    re_path(r'^company_summary/(?P<company_id>\d+)', views.company_summary, name='company-summary'),

]
