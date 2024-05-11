from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'quantity')
    list_display = ('name', 'quantity')
    ordering = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('user', 'date_ordered', 'completion_date', 'status')
    list_display = ('user', 'date_ordered', 'completion_date', 'status')
    ordering = ('status',)
    search_fields = ('user__username',)  # Wyszukiwanie po nazwie użytkownika
    list_filter = ('date_ordered', 'status')

# Jeśli korzystasz również z modelu OrderItem w panelu administracyjnym, dodaj odpowiednią definicję klasy tutaj
