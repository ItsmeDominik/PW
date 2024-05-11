from django.contrib import admin
from .models import Ticket, Comment


#admin.site.register(Room)
#admin.site.register(Room Reservation)

@admin.register(Ticket)
class Ticket(admin.ModelAdmin):
    fields = (('title'), 'description', 'status', 'category', 'room', 'user', 'priority', 'creation_time')
    list_display = ('title', 'category', 'status', 'user')
    ordering = ('status', 'priority')
    search_fields = ('user', 'title')
    list_filter = filter = ('priority',)

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    exclude = ('created_at',)
    fields = (('content'), 'created_at', 'ticket', 'user')
    list_display = ('content', 'created_at', 'ticket', 'user')
    ordering = ('created_at',)
    search_fields = ('ticket', 'user')
    list_filter = filter = ('created_at',)


