from django.contrib import admin
from .models import News
from .models import Discount


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = (('newsName'), 'publicationDate', 'description', 'newsCategory', 'author', 'newsImage')
    list_display = ('newsName', 'newsCategory', 'author')
    ordering = ('newsCategory',)
    search_fields = ('newsName', 'newsCategory', 'author')
    list_filter = filter = ('publicationDate',)\

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    fields = (('discount_title'), 'author', 'client', 'publicationDate', 'offer_Image', 'description')
    list_display = ('discount_title', 'author', 'client', 'publicationDate', 'description')
    ordering = ('publicationDate',)
    search_fields = ('client', 'author', 'discount_title')
    list_filter = filter = ('client',)