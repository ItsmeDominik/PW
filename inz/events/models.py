from django.db import models
from django.contrib.auth.models import User
from company.models import Company

class News(models.Model):
    NEWS_CATEGORY_CHOICES = [
        ('about_building', 'O Budynku'),
        ('building', 'Budynek'),
    ]
    newsName = models.CharField('Nazwa Wydarzenia', max_length=256)
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Autor")
    description = models.TextField('Opis')
    publicationDate = models.DateField('Data Publikacji')
    newsImage = models.ImageField('Zdjęcie', null=True, blank=True, upload_to='images')
    newsCategory = models.CharField(
        'Kategoria Wydarzenia',
        max_length=32,
        choices=NEWS_CATEGORY_CHOICES,
        default='building'
    )
    class Meta:
        verbose_name = 'Wydarzenie'
        verbose_name_plural = 'Wydarzenia'
    def __str__(self):
        return f"{self.newsName} | {self.get_newsCategory_display()} | {self.author.first_name} {self.author.last_name}"


class Discount(models.Model):
    discount_title = models.CharField('Tytuł Rabatu', max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    client = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Klient")
    publicationDate = models.DateField('Data Publikacji')
    offer_Image = models.ImageField('Zdjęcie', null=True, blank=True, upload_to='images')
    description = models.TextField('Opis Oferty')
    class Meta:
        verbose_name = 'Rabat'
        verbose_name_plural = 'Rabaty'
    def __str__(self):
        return f"{self.discount_title} | {self.author.username} | {self.client.companyName}"
