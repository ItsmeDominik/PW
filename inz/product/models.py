from django.db import models
from account.models import User

class Product(models.Model):
    name = models.CharField('Nazwa Produktu', max_length=200)
    quantity = models.PositiveIntegerField('Ilość')
    class Meta:
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkty'
    def __str__(self):
        return f"{self.name} | {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Ilość')
    date_ordered = models.DateTimeField('Data Zamówienia', null=True, blank=True)
    completion_date = models.DateTimeField('Data Realizacji', null=True, blank=True)
    ORDER_STATUS = [
        ('new', 'Oczekuje na realizację'),
        ('done', 'Zamówienie zostało zrealizowane'),
    ]
    status = models.CharField(
        'Status',
        max_length=32,
        choices=ORDER_STATUS,
        default='new',
    )
    def __str__(self):
        return f"Order {self.id} by {self.user.username} for {self.product.name} - {self.quantity}"
    class Meta:
        verbose_name = 'Zamówienia'
        verbose_name_plural = 'Zamówienia'


