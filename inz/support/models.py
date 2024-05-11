from django.db import models
from django.contrib.auth.models import User
from reservation.models import Room

class Comment(models.Model):
    content = models.TextField('Zawartość')
    created_at = models.DateTimeField('Data Utworzenia', auto_now_add=True)
    ticket = models.ForeignKey('Ticket', related_name='related_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Komentarze'
        verbose_name_plural = 'Komentarze'


class Ticket(models.Model):
    TICKET_CATEGORY_CHOICES = [('software', 'Software'), ('hardware', 'Hardware')]
    STATUS_CATEGORY_CHOICES = [('new', 'Nowy'), ('inProgress', 'W toku'), ('resolved', 'Rozwiązano')]
    PRIORITY_CATEGORY_CHOICES = [('low', 'Niski'), ('medium', 'Średni'), ('high', 'Wysoki')]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=200, choices=STATUS_CATEGORY_CHOICES, default='new')
    category = models.CharField(max_length=32, choices=TICKET_CATEGORY_CHOICES, default='software')
    priority = models.CharField(max_length=32, choices=PRIORITY_CATEGORY_CHOICES, default='low')
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Zgłoszenia'
        verbose_name_plural = 'Zgłoszenia'















