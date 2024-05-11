from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    BUSINESS_AREA_CHOICES = [
        ('design', 'Projektowanie'),
        ('it', 'IT'),
        ('co-working', 'Współpraca'),
        ('real estate', 'Nieruchomości'),
        ('customer service', 'Obsługa klienta'),
        ('data analysis', 'Analiza danych'),
        ('programming', 'Programowanie'),
        ('marketing', 'Marketing'),
        ('financed', 'Finanse'),
        ('insurance', 'Ubezpieczenia'),
        ('architecture', 'Architektura'),
    ]
    companyName = models.CharField('Nazwa Firmy', max_length=256)
    zipCode = models.CharField('Kod Pocztowy', max_length=10)
    location = models.CharField('Lokalizacja', max_length=256)
    nip = models.CharField('NIP', max_length=20)
    manager = models.ForeignKey(
        'account.Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_companies"
    )
    businessArea = models.CharField(
        'Obszar Działalności',
        max_length=32,
        choices=BUSINESS_AREA_CHOICES,
        default='customer service'
    )
    def __str__(self):
        return f"{self.companyName} ({self.get_businessArea_display()})"
    class Meta:
        verbose_name = 'Firma'
        verbose_name_plural = 'Firmy'
