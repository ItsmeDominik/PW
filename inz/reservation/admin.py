from django.contrib import admin
from .models import Room
from .models import RoomReservation
from .models import OfficeRoomReservation
from .models import Printers
from .models import PrinterRent

@admin.register(Room)
class Room(admin.ModelAdmin):
    fields = (('name'), 'description', 'capacity', 'location', 'price', 'destination')
    list_display = ('name', 'location', 'capacity', 'price', 'destination')
    ordering = ('capacity',)
    search_fields = ('name', 'capacity', 'location')
    filter = ('capacity', 'destination')


@admin.register(RoomReservation)
class RoomReservation(admin.ModelAdmin):
    fields = (('room'), 'date', 'start_time', 'end_time', 'user', 'company', 'cost', 'discount')
    list_display = ('room', 'user', 'date', 'start_time', 'end_time', 'company', 'cost', 'discount')
    ordering = ('start_time',)
    search_fields = ('room', 'user', 'date')
    list_filter = filter = ('date',)

@admin.register(OfficeRoomReservation)
class OfficeRoomReservation(admin.ModelAdmin):
    fields = (('room'), 'start_date', 'end_date', 'user', 'company', 'cost', 'discount')
    list_display = ('room', 'user', 'start_date', 'end_date', 'company', 'cost', 'discount')
    ordering = ('start_date',)
    search_fields = ('room', 'user')
    list_filter = filter = ('cost',)

@admin.register(Printers)
class Printers(admin.ModelAdmin):
    fields = (('model', 'serial_number'), 'price', 'date_of_last_service', 'date_of_next_service', 'status')
    list_display = ('model', 'serial_number', 'price', 'date_of_last_service', 'date_of_next_service', 'status')
    ordering = ('price','status')
    search_fields = ('model',)
    list_filter = filter = ('price',)

@admin.register(PrinterRent)
class PrinterRent(admin.ModelAdmin):
    fields = (('printer'), 'start_date', 'end_date', 'user', 'company', 'cost', 'number_of_page', 'discount')
    list_display = ('printer', 'user', 'start_date', 'end_date', 'company', 'cost', 'number_of_page', 'discount')
    ordering = ('start_date',)
    search_fields = ('user', 'printer')
    list_filter = filter = ('cost',)

