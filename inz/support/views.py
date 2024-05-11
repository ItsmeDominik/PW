from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .models import Ticket, Comment
from .forms import UpdateTicketForm
from django.utils import timezone

# Importowanie wymaganych dekoratorów i innych modułów
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .forms import NewTicketForm

# Definicja funkcji widoku odpowiedzialnej za dodawanie nowych zgłoszeń wsparcia technicznego
@login_required  # Wymaganie zalogowania
@permission_required('support.add_ticket', raise_exception=True)  # Wymaganie odpowiednich uprawnień
def add_SupportTicket(request):
    # Inicjalizacja zmiennej określającej, czy formularz został przesłany
    submitted = False

    # Obsługa żądania typu POST
    if request.method == "POST":
        form = NewTicketForm(request.POST)  # Inicjalizacja formularza z danymi POST
        if form.is_valid():  # Walidacja formularza
            ticket = form.save(commit=False)  # Zapisanie formularza bez commitowania
            ticket.user = request.user  # Przypisanie użytkownika do zgłoszenia
            ticket.save()  # Zapisanie zgłoszenia w bazie danych
            return redirect('list-tickets')  # Przekierowanie do listy zgłoszeń

    # Obsługa innych typów żądań (np. GET)
    else:
        form = NewTicketForm()  # Inicjalizacja pustego formularza
        if 'submitted' in request.GET:  # Sprawdzenie, czy formularz został przesłany
            submitted = True

    # Renderowanie szablonu HTML z formularzem
    return render(request, 'support/add_support_ticket.html', {'form': form, 'submitted': submitted})


@login_required
@permission_required('support.view_ticket', raise_exception=True)
def listTickets(request):
    status = request.GET.get('status', None)
    if request.user.is_superuser:
        if status:
            ticket_list = Ticket.objects.filter(status=status).order_by('status')
        else:
            ticket_list = Ticket.objects.all().order_by('status')
    else:
        if status:
            ticket_list = Ticket.objects.filter(user=request.user, status=status).order_by('status')
        else:
            ticket_list = Ticket.objects.filter(user=request.user).order_by('status')

    p = Paginator(ticket_list, 2)
    page = request.GET.get('page')
    tickets = p.get_page(page)

    return render(request, 'support/list_tickets.html', {'tickets': tickets})

@login_required
@permission_required('support.view_ticket', raise_exception=True)
def showTicket(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    return render(request, 'support/show_ticket.html', {'ticket': ticket })

@login_required
@permission_required('support.add_comment', raise_exception=True)
def add_comment(request, ticket_id):
    if request.method == 'POST':
        ticket = Ticket.objects.get(pk=ticket_id)
        user = request.user

        content = request.POST.get('content')

        comment = Comment(content=content, user=user, ticket=ticket)
        comment.save()

        # Check if the user is in the group "admin"
        if user.groups.filter(name='admin').exists():
            return redirect('update-ticket', ticket_id=ticket.id)
        else:
            return redirect('show-ticket', ticket_id=ticket.id)

    return redirect('home')


@login_required
@permission_required('support.view_ticket', raise_exception=True)
def list_support_tickets(request):
    status = request.GET.get('status', None)
    if status:
        ticket_list = Ticket.objects.filter(status=status).order_by('status')
    else:
        ticket_list = Ticket.objects.all().order_by('status')

    p = Paginator(ticket_list, 2)
    page = request.GET.get('page')
    tickets = p.get_page(page)

    return render(request, 'support/list_support_tickets.html', {'tickets': tickets})

@login_required
@permission_required('support.view_ticket', raise_exception=True)
def list_new_tickets(request):
    priority = request.GET.get('priority', None)
    if priority:
        ticket_list = Ticket.objects.filter(status='new', priority=priority).order_by('status')
    else:
        ticket_list = Ticket.objects.filter(status='new').order_by('status')
    p = Paginator(ticket_list, 2)
    page = request.GET.get('page')
    tickets = p.get_page(page)
    return render(request, 'support/list_new_tickets.html', {'tickets': tickets})

@login_required
@permission_required('support.view_ticket', raise_exception=True)
def list_in_progress_tickets(request):
    priority = request.GET.get('priority', None)
    if priority:
        ticket_list = Ticket.objects.filter(status='inProgress', priority=priority).order_by('status')
    else:
        ticket_list = Ticket.objects.filter(status='inProgress').order_by('status')
    p = Paginator(ticket_list, 2)
    page = request.GET.get('page')
    tickets = p.get_page(page)
    return render(request, 'support/list_in_progress_tickets.html', {'tickets': tickets})

@login_required
@permission_required('support.view_ticket', raise_exception=True)
def list_resolved_tickets(request):
    priority = request.GET.get('priority', None)
    if priority:
        ticket_list = Ticket.objects.filter(status='resolved', priority=priority).order_by('status')
    else:
        ticket_list = Ticket.objects.filter(status='resolved').order_by('status')
    p = Paginator(ticket_list, 2)
    page = request.GET.get('page')
    tickets = p.get_page(page)
    return render(request, 'support/list_resolved_tickets.html', {'tickets': tickets})

@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = UpdateTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            status = form.cleaned_data['status']
            if status == 'resolved' and not ticket.end_time:
                ticket.end_time = timezone.now()
            ticket.save()
            return redirect('update-ticket', ticket_id=ticket.id)
    else:
        form = UpdateTicketForm(instance=ticket)

    return render(request, 'support/update_ticket.html', {'form': form, 'ticket': ticket})


