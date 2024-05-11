from django.shortcuts import render, redirect, get_object_or_404

from account.models import Account
from company.models import Company
from .models import  News, Discount
from .forms import NewsForm, NewsFormAdmin,  DiscountForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
#News

from datetime import date



@login_required
@permission_required('events.add_discount', raise_exception=True)
def add_discount(request):
    # Obsługa żądania typu POST
    if request.method == 'POST':
        # Inicjalizacja formularza z danymi z żądania
        form = DiscountForm(request.POST, request.FILES)
        # Walidacja formularza
        if form.is_valid():
            # Zapisanie obiektu rabatu z pominięciem commitowania
            discount = form.save(commit=False)
            # Uzupełnienie dodatkowych pól obiektu rabatu
            discount.author = request.user
            discount.publicationDate = date.today()
            # Zapisanie obiektu rabatu w bazie danych
            discount.save()
            # Pobranie company_id i przekierowanie do strony z listą rabatów
            company_id = discount.client.id
            return redirect('list-discount', company_id=company_id)
    # Inicjalizacja pustego formularza dla żądań innych niż POST
    else:
        form = DiscountForm()
    # Renderowanie strony z formularzem
    return render(request, 'events/add_discount.html', {'form': form})


@login_required
@permission_required('events.delete_discount', raise_exception=True)
def delete_discount(request, discount_id):
    discount = Discount.objects.get(pk=discount_id)
    company_id = discount.client.id  # Pobierz ID firmy przypisanej do rabatu

    if request.user == discount.author or request.user.is_superuser:
        discount.delete()
        messages.success(request, ("Rabat został usunięty!"))
        return redirect('list-discount', company_id=company_id)  # Przekieruj z company_id
    else:
        messages.success(request, ("Nie jesteś upoważniony do usunięcia tego rabatu!"))
        return redirect('list-discount', company_id=company_id)  # Przekieruj z company_id


@login_required
@permission_required('events.change_discount', raise_exception=True)
def update_discount(request, discount_id):
    discount = Discount.objects.get(pk=discount_id)
    company_id = discount.client.id  # Pobierz ID firmy przypisanej do rabatu

    form = DiscountForm(request.POST or None, request.FILES or None, instance=discount)
    if form.is_valid():
        form.save()
        return redirect('list-discount', company_id=company_id)  # Przekieruj z company_id

    return render(request, 'events/update_discount.html', {'discount': discount, 'form': form})
@login_required
@permission_required('events.view_discount', raise_exception=True)
def list_discount(request, company_id=None):
    # Jeśli company_id nie jest podane, użyj firmy zalogowanego użytkownika
    if company_id is None:
        account = Account.objects.get(user=request.user)
        company = account.company
    else:
        company = Company.objects.get(id=company_id)

    # Filtruj rabaty na podstawie firmy
    discounts = Discount.objects.filter(client=company).order_by('publicationDate')

    p = Paginator(discounts, 4)
    page = request.GET.get('page')
    discounts_paginated = p.get_page(page)

    return render(request, 'events/list_discount.html', {'discount': discounts_paginated})


@login_required
@permission_required('events.view_discount', raise_exception=True)
def show_discount(request, discount_id):
    discount = Discount.objects.get(pk=discount_id)
    return render(request, 'events/show_discount.html', {'discount': discount})
@login_required
@permission_required('events.add_news', raise_exception=True)
def add_news(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = NewsFormAdmin(request.POST, request.FILES)
        else:
            form = NewsForm(request.POST, request.FILES)  # Dodaj tutaj request.FILES
        if form.is_valid():
            news = form.save(commit=False)
            if not request.user.is_superuser:
                news.author = request.user
            news.save()
            return redirect('list-news')

    else:
        if request.user.is_superuser:
            form = NewsFormAdmin()
        else:
            form = NewsForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_news.html', {'form': form, 'submitted': submitted})


@login_required
@permission_required('events.delete_news', raise_exception=True)
def delete_news(request, news_id):
    news = News.objects.get(pk=news_id)
    if request.user == news.author or request.user.is_superuser:
        news.delete()
        messages.success(request, ("Wiadomość została usunięta!"))
        return redirect('list-update-news')
    else:
        messages.success(request, ("Nie jesteś upoważniony do usunięcia tej wiadomości!"))
        return redirect('list-news')


@login_required
@permission_required('events.change_news', raise_exception=True)
def update_news(request, news_id):
    news = News.objects.get(pk=news_id)
    if request.user.is_superuser:
        form = NewsFormAdmin(request.POST or None, request.FILES or None, instance=news)
    else:
        form = NewsForm(request.POST or None, request.FILES or None, instance=news)
    if form.is_valid():
        form.save()
        return redirect('list-update-news')
    return render(request, 'events/update_news.html', {'news': news, 'form': form})

@login_required
@permission_required('events.view_news', raise_exception=True)
def show_news(request, news_id):
    news = News.objects.get(pk=news_id)
    return render(request, 'events/show_news.html', {'news': news })

@login_required
@permission_required('events.view_news', raise_exception=True)
def list_news_update(request):
    if request.user.is_superuser:
        news_list = News.objects.all().order_by('publicationDate')
    else:
        news_list = News.objects.filter(author=request.user).order_by('publicationDate')
    p = Paginator(news_list, 6)
    page = request.GET.get('page')
    news_update = p.get_page(page)
    return render(request, 'events/list_news_update.html', {'news_update': news_update})

@login_required
@permission_required('events.view_news', raise_exception=True)
def list_news(request):
    p = Paginator(News.objects.all().order_by('publicationDate'), 6)
    page = request.GET.get('page')
    news = p.get_page(page)
    return render(request, 'events/news.html', {'news': news})






