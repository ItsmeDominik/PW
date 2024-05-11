from django import forms
from django.forms import ModelForm
from .models import Ticket

class NewTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'category', 'room', 'priority')
        labels = {
            'title': 'Tytuł Zgłoszenia',
            'description': 'Opis',
            'category': 'Kategoria',
            'room': 'Pomieszczenie',
            'priority': 'Priorytet',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tytuł'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Opis'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        labels = {
            'status': 'Aktualizuj Staus Zgłoszenia',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),

        }
