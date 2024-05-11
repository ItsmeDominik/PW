from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group
from .models import Company, Account
from django.utils.translation import gettext as _

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label=_("Nazwa użytkownika"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label=_("Twój adres email"),
        widget=forms.EmailInput(attrs={'class':'form-control'})
    )
    first_name = forms.CharField(
        label=_("Imię"),
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    last_name = forms.CharField(
        label=_("Nazwisko"),
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    company = forms.ModelChoiceField(
        label=_("Firma"),
        queryset=Company.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    position = forms.CharField(
        label=_("Stanowisko"),
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    group = forms.ModelChoiceField(
        label=_("Członek grupy:"),
        queryset=Group.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    contact_person = forms.ChoiceField(
        choices=Account.CONTACT_CHOICES,
        label=_("Czy użytkownik jest osobą kontaktową?"),
        widget=forms.RadioSelect()  # Używaj RadioSelect dla wyraźniejszego wyboru między 'Tak' i 'Nie'
    )

    is_staff = forms.BooleanField(
        label=_("Czy użytkownik ma mieć dostęp do panelu administracyjnego?"),
        required=False,
        widget=forms.CheckboxInput()
    )
    is_superuser = forms.BooleanField(
        label=_("Czy użytkownik jest administratorem?"),
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'company', 'position', 'group', 'contact_person', 'is_staff', 'is_superuser')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = _("Hasło")
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = _("Potwierdź hasło")
