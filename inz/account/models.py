from django.db import models
from django.contrib.auth.models import User
from company.models import Company

class Account(models.Model):
    CONTACT_CHOICES = [
        ('yes', 'Tak'),
        ('no', 'Nie'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Firma")
    position = models.CharField('Pozycja', max_length=256)
    contact_person = models.CharField(
        'Osoba Kontaktowa',
        max_length=32,
        choices=CONTACT_CHOICES,
        default='no'
    )
    class Meta:
        verbose_name = 'Konto'
        verbose_name_plural = 'Konta'
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
