from django import forms
from .models import Order, Product
from django.utils import timezone

class OrderForm(forms.ModelForm):
    date_ordered = forms.DateTimeField(initial=timezone.now, required=False, widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = ['user', 'product', 'quantity', 'status', 'completion_date', 'date_ordered']
        labels = {
            'product': 'Produkt',
            'quantity': 'Ilość',
            'status': 'Status',
            'completion_date': 'Data realizacji',
            'date_ordered': 'Data zamówienia',
        }
        widgets = {
            'user': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'completion_date': forms.HiddenInput(),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ilość'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity']
        labels = {
            'name': 'Nazwa Produktu',
            'quantity': 'Ilość',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa produktu'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ilość'}),
        }
