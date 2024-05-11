from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from account.models import Account
import re
from .models import Company

class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        admin_group = Group.objects.get(name='administration')
        # Filtruj użytkowników z grupy "administration"
        admin_accounts = Account.objects.filter(user__groups=admin_group)
        self.fields['manager'].queryset = admin_accounts

    class Meta:
        model = Company
        fields = ('companyName', 'manager', 'zipCode', 'location', 'nip', 'businessArea')
        labels = {
            'companyName': 'Nazwa Firmy:',
            'manager': 'Opiekun:',
            'zipCode': 'Kod Pocztowy:',
            'location': 'Lokalizacja:',
            'nip': 'NIP:',
            'businessArea': 'Obszar działalności:',
        }
        widgets = {
            'companyName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa Firmy'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'zipCode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kod Pocztowy'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lokalizacja'}),
            'nip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIP'}),
            'businessArea': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_zipCode(self):
        zipCode = self.cleaned_data['zipCode']
        if not re.match(r'^\d{2}-\d{3}$', zipCode):
            raise ValidationError('Invalid ZIP code - it should be in XX-XXX format.')
        return zipCode

    def clean_nip(self):
        nip = self.cleaned_data['nip']
        if not re.match(r'^\d{10}$', nip):
            raise ValidationError('Invalid NIP - it should be exactly 10 digits.')
        return nip
