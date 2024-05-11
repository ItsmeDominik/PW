from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from account.form import RegisterUserForm
from . models import Account
from . models import Company


def login_user(request):
    # Jeśli użytkownik jest już zalogowany, przekieruj go na stronę główną
    if request.user.is_authenticated:
        return redirect('list-news')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list-news')
        else:
            messages.success(request, ("Wystąpił błąd podczas logowania, spróbuj ponownie..."))
            return redirect('login-user')

    else:
        return render(request, 'authenticate/login.html', {})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login-user')

@login_required
@permission_required('account.add_account', raise_exception=True)
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Nie zapisuj jeszcze użytkownika
            user.is_staff = form.cleaned_data['is_staff']  # Dodaj informację o statusie staff
            user.save()  # Teraz zapisz użytkownika

            group = form.cleaned_data['group']  # pobierz grupę z formularza
            if group:
                group.user_set.add(user)  # dodaj użytkownika do grupy

            # Pobierz wartość contact_person z formularza
            contact_person_value = form.cleaned_data['contact_person']

            account = Account(
                user=user,
                company=form.cleaned_data['company'],
                position=form.cleaned_data['position'],
                contact_person=contact_person_value  # Dodaj tę wartość do modelu
            )
            account.save()
            return redirect('list-news')
    else:
        form = RegisterUserForm()

    return render(request, 'authenticate/register.html', {'form': form})


@login_required
@permission_required('account.view_account', raise_exception=True)
def list_users(request):
    accounts = Account.objects.all()
    return render(request, 'authenticate/list_users.html', {'accounts': accounts})


# Importy i dekoratory uprawnień
@login_required
@permission_required('account.view_account', raise_exception=True)
def list_company_users(request, company_id):
    # Pobranie wszystkich kont użytkowników dla danej firmy
    # Sortowanie kont według pola contact_person w odwrotnej kolejności
    company_accounts = Account.objects.filter(
        company_id=company_id
    ).order_by('-contact_person')
    # Pobranie informacji o firmie na podstawie company_id
    company = Company.objects.get(id=company_id)
    # Ustalenie kontekstu dla szablonu HTML
    context = {
        'accounts': company_accounts,
        'company': company
    }
    # Renderowanie strony z listą użytkowników
    return render(request, 'authenticate/list_users.html', context)




