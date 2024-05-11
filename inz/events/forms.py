from .models import News
from django.forms import ModelForm
from datetime import datetime
import pytz
from django import forms
from .models import Discount

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ('discount_title', 'client', 'description', 'offer_Image') # Usunięte 'author' i 'publicationDate'
        labels = {
            'discount_title': 'Tytuł Oferty',
            'client': 'Klient',
            'description': 'Opis',
            'offer_Image': 'Zdjęcie',
        }
        widgets = {
            'discount_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tytuł Rabatu'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'offer_Image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Opis Rabatu'}),
        }

# Create a news form
class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = ('newsName', 'description', 'newsCategory', 'newsImage','publicationDate')
        labels = {
            'newsName': 'Nazwa Wydarzenia',
            'description': 'Opis',
            'newsCategory': 'Kategoria Wydarzenia',
            'newsImage': 'Zdjęcie',
            'publicationDate': 'Data Publikacji',
        }
        widgets = {
            'newsName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa Wydarzenia'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Opis'}),
            'newsCategory': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

        # Set the publicationDate field to today's date
        tz = pytz.timezone('Europe/Warsaw')
        now = datetime.now(tz)
        self.initial['publicationDate'] = now.date()
        self.fields['publicationDate'].widget = forms.TextInput(attrs={'readonly': 'readonly'})  # Make publicationDate field readonly

class NewsFormAdmin(ModelForm):
    class Meta:
        model = News
        fields = ('newsName', 'description', 'newsCategory', 'author', 'newsImage', 'publicationDate')
        labels = {
            'newsName': 'Nazwa Wydarzenia',
            'description': 'Opis',
            'newsCategory': 'Kategoria Wydarzenia',
            'author': 'Autor',
            'newsImage': 'Zdjęcie',
            'publicationDate': 'Data Publikacji',
        }
        widgets = {
            'newsName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'News name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'newsCategory': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(NewsFormAdmin, self).__init__(*args, **kwargs)

        # Set the publicationDate field to today's date
        tz = pytz.timezone('Europe/Warsaw')
        now = datetime.now(tz)
        self.initial['publicationDate'] = now.date()
        self.fields['publicationDate'].widget = forms.TextInput(attrs={'readonly': 'readonly'})  # Make publicationDate field readonly
