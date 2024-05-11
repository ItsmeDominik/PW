import datetime
from account.models import Account
from company.models import Company
from .forms import RoomReservationForm, RoomForm, OfficeRentForm, PrinterForm, PrinterRentForm
from django.core.paginator import Paginator
from .models import Room
from datetime import datetime, time,timedelta
import pytz
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import RoomReservation, OfficeRoomReservation, Printers, PrinterRent
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from datetime import date
timezone = pytz.timezone('Europe/Warsaw')
from functools import wraps


def all_permissions_required(view_func):
    """
    Dekorator wymagający, aby użytkownik był zalogowany i miał wszystkie wymagane uprawnienia.
    """
    @wraps(view_func)
    @login_required
    @permission_required('reservation.view_printerrent', raise_exception=True)
    @permission_required('reservation.view_officeroomreservation', raise_exception=True)
    @permission_required('reservation.view_roomreservation', raise_exception=True)
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Następnie możesz użyć tego dekoratora w następujący sposób:

@all_permissions_required
def company_summary(request, company_id):
    # Pobierz obiekt firmy na podstawie company_id
    company = Company.objects.get(id=company_id)
    today = date.today()
    # Pobierz liczbę wynajętych drukarek dla firmy, których data zakończenia wynajmu jest w tym samym dniu
    # lub później niż dzisiejsza data
    rented_printers_count = PrinterRent.objects.filter(company=company, end_date__gte=today).count()
    # Pobierz liczbę zarezerwowanych pomieszczeń dla firmy, których data rezerwacji jest w tym samym dniu
    # lub później niż dzisiejsza data
    reserved_rooms_count = RoomReservation.objects.filter(company=company, date__gte=today).count()
    # Pobierz liczbę zarezerwowanych sal konferencyjnych dla firmy, których data zakończenia wynajmu jest w tym samym dniu
    # lub później niż dzisiejsza data
    reserved_office_rooms_count = OfficeRoomReservation.objects.filter(company=company, end_date__gte=today).count()
    # Przekazanie danych do szablonu
    context = {
        'company': company,
        'rented_printers_count': rented_printers_count,
        'reserved_rooms_count': reserved_rooms_count,
        'reserved_office_rooms_count': reserved_office_rooms_count,
    }
    return render(request, 'reservation/company_summary.html', context)



@login_required
@permission_required('reservation.view_printers', raise_exception=True)
def my_printers(request):
    # Pobierz konto zalogowanego użytkownika
    user_account = Account.objects.get(user=request.user)

    # Pobierz firmę zalogowanego użytkownika
    user_company = user_account.company

    # Znajdź wszystkie rezerwacje drukarek dla tej firmy
    printer_reservations = PrinterRent.objects.filter(company=user_company)
    paginator = Paginator(printer_reservations, 2)  # Pokaż 2 rezerwacje na stronie (zmieniłem z 6 na 2 dla spójności z kodem)
    page = request.GET.get('page')
    printers = paginator.get_page(page)
    return render(request, 'reservation/my_printers.html', {'printers': printers})


@login_required
@permission_required('reservation.change_printers', raise_exception=True)
def update_printer(request, printer_id):
    printer = Printers.objects.get(pk=printer_id)
    form = PrinterForm(request.POST or None, instance=printer)
    if form.is_valid():
        form.save()
        return redirect('list-update-printer')
    return render(request, 'reservation/update_printer.html', {'news': printer, 'form': form})

@login_required
@permission_required('reservation.change_printers', raise_exception=True)
def update_printer_status(request, printer_id):
    printer = Printers.objects.get(pk=printer_id)
    form = PrinterForm(request.POST or None, instance=printer)
    if form.is_valid():
        form.save()
        return redirect('list-update-printer')
    return render(request, 'reservation/update_printer.html', {'news': printer, 'form': form})
@login_required
@permission_required('reservation.delete_printers', raise_exception=True)
def delete_printer(request, printer_id):
    printer = get_object_or_404(Printers, pk=printer_id)
    printer.delete()
    messages.success(request, "Drukarka została usunięta!")

    return redirect('list-update-printer')  # Przekierowanie do URL o nazwie 'my-reservations'
@login_required
@permission_required('reservation.view_printers', raise_exception=True)
def list_update_printer(request):
    printer_list = Printers.objects.all().order_by('model')
    paginator = Paginator(printer_list, 2)  # Pokaż 6 drukarek na stronie
    page = request.GET.get('page')
    printers = paginator.get_page(page)
    destination = 'update'
    return render(request, 'reservation/list_update_printer.html', {'printers': printers, 'destination': destination})

@login_required
@permission_required('reservation.view_printers', raise_exception=True)
def list_printers(request):
    printer_list = Printers.objects.all().order_by('model')
    paginator = Paginator(printer_list, 2)  # Pokaż 6 drukarek na stronie
    page = request.GET.get('page')
    printers = paginator.get_page(page)
    return render(request, 'reservation/list_printers.html', {'printers': printers})

@login_required
@permission_required('reservation.view_printers', raise_exception=True)
def list_rent_printer(request):
    printer_list = Printers.objects.filter(status='unused').order_by('price')
    paginator = Paginator(printer_list, 2)  # Pokaż 6 drukarek na stronie
    page = request.GET.get('page')
    printers = paginator.get_page(page)
    destination = 'rent'
    return render(request, 'reservation/list_update_printer.html', {'printers': printers, 'destination': destination})

@login_required
@permission_required('reservation.view_printerrent', raise_exception=True)
def list_rented_printer(request):
    printer_list = PrinterRent.objects.order_by('cost')
    paginator = Paginator(printer_list, 2)  # Pokaż 6 drukarek na stronie
    page = request.GET.get('page')
    printerRent = paginator.get_page(page)
    return render(request, 'reservation/list_rented_printer.html', {'printerRent': printerRent})

@login_required
@permission_required('reservation.view_printerrent', raise_exception=True)
def expired_rented_printers(request):
    expired_printers_list = PrinterRent.objects.filter(end_date__lt=date.today(), printer__status='in_use')

    # Dodaj stronicowanie
    paginator = Paginator(expired_printers_list, 2)  # Na przykład, pokazuj 6 drukarek na stronie
    page = request.GET.get('page')
    expired_printers = paginator.get_page(page)

    return render(request, 'reservation/expired_rented_printers.html', {'expired_printers': expired_printers})

@login_required
@permission_required('reservation.change_printers', raise_exception=True)
def update_printer_status_expired(request, printer_id):
    # Pobierz obiekt drukarki o określonym ID
    printer = get_object_or_404(Printers, id=printer_id)

    # Zaktualizuj status drukarki na 'unused'
    printer.status = 'unused'
    printer.save()

    # Przekieruj użytkownika z powrotem do strony (lub innej strony według życzenia)
    return redirect('expired-rented-printers')  # Zastąp odpowiednią nazwą URL-a


@login_required
@permission_required('reservation.add_printerrent', raise_exception=True)
def add_printer_rent(request, printer_id):
    printer = Printers.objects.get(pk=printer_id)

    if request.method == "POST":
        form = PrinterRentForm(request.POST, user=request.user, printer=printer)
        if form.is_valid():
            printer_rent = form.save()
            printer.status = 'in_use'  # Ustaw status drukarki na "in_use"
            printer.save()  # Zapisz zmieniony status drukarki
            return redirect('list-rent-printer')
    else:
        form = PrinterRentForm(user=request.user, printer=printer)

    return render(request, 'reservation/add_printer_rent.html', {
        'form': form,
        'printer_model': printer.model,
    })

@login_required
@permission_required('reservation.add_printers', raise_exception=True)
def add_printer(request):
    if request.method == "POST":
        form = PrinterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list-update-printer')  # replace with your own success redirect
    else:
        form = PrinterForm()
    return render(request, 'reservation/add_printer.html', {'form': form})
@login_required
@permission_required('reservation.view_room', raise_exception=True)
def list_office_rooms(request):
    p = Paginator(Room.objects.filter(destination='office').order_by('location'), 4)
    page = request.GET.get('page')
    destination = 'office'
    rooms = p.get_page(page)
    return render(request, 'reservation/rooms.html', {'rooms': rooms, 'destination': destination})

@login_required
@permission_required('reservation.view_room', raise_exception=True)
def list_reservation_rooms(request):
    # Filtruj pokoje na podstawie wartości 'conference_room' w polu destination
    p = Paginator(Room.objects.filter(destination='conference_room').order_by('capacity'), 4)
    page = request.GET.get('page')
    destination = 'conference_room'
    rooms = p.get_page(page)
    return render(request, 'reservation/rooms.html', {'rooms': rooms, 'destination': destination})


@login_required
@permission_required('reservation.view_room', raise_exception=True)
def list_rooms(request):
    p = Paginator(Room.objects.all().order_by('capacity'), 5)
    page = request.GET.get('page')
    room = p.get_page(page)
    return render(request, 'reservation/rooms.html', {'room': room})

@login_required
@permission_required('reservation.view_room', raise_exception=True)
def show_rooms(request, room_id):
    room = Room.objects.get(pk=room_id)
    return render(request, 'reservation/show_room.html', {'room': room,})

@login_required
@permission_required('reservation.add_roomreservation', raise_exception=True)
def add_RoomReservation(request, room_id):
    room = Room.objects.get(pk=room_id)
    date = datetime.now().date()
    submitted = False
    if request.method == "POST":
        form = RoomReservationForm(request.POST, request.FILES, room=room)
        if form.is_valid():
            roomReservation = form.save(commit=False)
            roomReservation.user = request.user
            roomReservation.room = room
            roomReservation.date = date
            roomReservation.save()
            return redirect('my-reservations')
    else:
        form = RoomReservationForm(room=room)
        submitted = 'submitted' in request.GET
    reservations = RoomReservation.objects.filter(date=date, room_id=room_id).order_by('start_time')
    timeline_data = generate_timeline_data(reservations)
    return render(request, 'reservation/add_reservation.html', {
        'form': form,
        'submitted': submitted,
        'timeline_data': timeline_data,
        'current_date': date.strftime('%d %B'),
        'room_name': room.name
    })


# Importy Django dla mechanizmów autentykacji i autoryzacji
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .models import Room, OfficeRoomReservation
from .forms import OfficeRentForm


# Dekorator login_required sprawdza, czy użytkownik jest zalogowany.
# Dekorator permission_required sprawdza, czy użytkownik ma uprawnienia do dodania rezerwacji.
# Parametr raise_exception=True spowoduje, że zostanie wywołany wyjątek, jeśli użytkownik nie ma uprawnień.
@login_required
@permission_required('reservation.add_officeroomreservation', raise_exception=True)
def add_OfficeRent(request, room_id):
    # Pobieranie informacji o pokoju na podstawie przekazanego identyfikatora (room_id).
    room = Room.objects.get(pk=room_id)

    # Pobieranie istniejących rezerwacji dla danego pokoju.
    existing_reservations = OfficeRoomReservation.objects.filter(room=room)

    # Obsługa żądania POST od formularza.
    if request.method == "POST":
        form = OfficeRentForm(request.POST, request.FILES, user=request.user, room=room)
        if form.is_valid():
            # Zapisanie nowej rezerwacji i przekierowanie do strony 'my-rents'.
            form.save()
            return redirect('my-rents')
    else:
        # Inicjalizacja pustego formularza.
        form = OfficeRentForm(user=request.user, room=room)

    # Wyrenderowanie strony z formularzem.
    return render(request, 'reservation/add_rent.html', {
        'form': form,
        'room_name': room.name,
        'existing_reservations': existing_reservations
    })


@login_required
@permission_required('reservation.view_officeroomreservation', raise_exception=True)
def myRents(request):
    current_date = datetime.now(pytz.timezone('Europe/Warsaw'))
    room_name = request.GET.get('room', None)

    # Pobranie obiektu Account dla zalogowanego użytkownika
    user_account = Account.objects.get(user=request.user)

    base_filters = {
        'end_date__gte': current_date
    }

    if room_name:
        base_filters['room__name'] = room_name

    # Check if the user is part of the 'administration' group
    if request.user.groups.filter(name='administration').exists():
        reservation_list = OfficeRoomReservation.objects.filter(**base_filters).order_by('start_date')
    # Check if the user is part of the 'admin' group
    elif request.user.groups.filter(name='admin').exists():
        reservation_list = OfficeRoomReservation.objects.filter(**base_filters).order_by('start_date')
    # Check if the user is part of the 'client' group
    elif request.user.groups.filter(name='client').exists():
        base_filters['company'] = user_account.company
        reservation_list = OfficeRoomReservation.objects.filter(**base_filters).order_by('start_date')

    p = Paginator(reservation_list, 2)
    page = request.GET.get('page')
    reservations = p.get_page(page)
    room_names = Room.objects.values_list('name', flat=True)

    return render(request, 'reservation/my_rents.html', {'reservations': reservations, 'room_names': room_names})


@login_required
@permission_required('reservation.view_roomreservation', raise_exception=True)
def myReservations(request):
    current_date = datetime.now(pytz.timezone('Europe/Warsaw'))
    room_name = request.GET.get('room', None)

    # Pobranie obiektu Account dla zalogowanego użytkownika
    user_account = Account.objects.get(user=request.user)

    # Check if the user is part of the 'administration' group
    if request.user.groups.filter(name='administration').exists():
        if room_name:
            reservation_list = RoomReservation.objects.filter(date=current_date, room__name=room_name).order_by(
                'start_time')
        else:
            reservation_list = RoomReservation.objects.filter(date=current_date).order_by('start_time')
    # Check if the user is part of the 'administration' group
    elif request.user.groups.filter(name='admin').exists():
        if room_name:
            reservation_list = RoomReservation.objects.filter(date=current_date, room__name=room_name).order_by(
                'start_time')
        else:
            reservation_list = RoomReservation.objects.filter(date=current_date).order_by('start_time')
    # Check if the user is part of the 'client' group
    elif request.user.groups.filter(name='client').exists():
        if room_name:
            reservation_list = RoomReservation.objects.filter(company=user_account.company, date=current_date,
                                                              room__name=room_name).order_by('start_time')
        else:
            reservation_list = RoomReservation.objects.filter(company=user_account.company, date=current_date).order_by(
                'start_time')


    p = Paginator(reservation_list, 2)
    page = request.GET.get('page')
    reservations = p.get_page(page)
    room_names = Room.objects.values_list('name', flat=True)
    return render(request, 'reservation/my_reservations.html', {'reservations': reservations, 'room_names': room_names})


@login_required
@permission_required('reservation.delete_roomreservation', raise_exception=True)
def deleteReservation(request, reservation_id):
    reservation = get_object_or_404(RoomReservation, pk=reservation_id)
    if request.user == reservation.user:
        reservation.delete()
        messages.success(request, "Rezerwacja została anulowana!")
    else:
        messages.error(request, "You aren't authorized to delete this reservation!")
    return redirect('my-reservations')  # Przekierowanie do URL o nazwie 'my-reservations'
@login_required
@permission_required('reservation.add_room', raise_exception=True)
def add_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list-update-room')  # replace with your own success redirect
    else:
        form = RoomForm()
    return render(request, 'reservation/add_room.html', {'form': form})

@login_required
@permission_required('reservation.change_room', raise_exception=True)
def update_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    form = RoomForm(request.POST or None, request.FILES or None, instance=room)
    if form.is_valid():
        form.save()
        return redirect('list-update-room')
    return render(request, 'reservation/update_room.html', {'room': room, 'form': form})

@login_required
@permission_required('reservation.view_room', raise_exception=True)
def list_update_room(request):
    if request.user.is_superuser:
        room_list = Room.objects.all().order_by('location')

        # Filtruj pokoje na podstawie parametru 'destination' w URL
        destination_filter = request.GET.get('destination')
        if destination_filter:
            room_list = room_list.filter(destination=destination_filter)

        p = Paginator(room_list, 4)
        page = request.GET.get('page')
        rooms = p.get_page(page)
        return render(request, 'reservation/list_update_room.html', {'rooms': rooms})
    else:
        messages.success(request, ("You aren't authorized to do this!"))

@login_required
@permission_required('reservation.view_room', raise_exception=True)
def list_update_office(request):
    if request.user.is_superuser:
        room_list = Room.objects.filter(destination='office').order_by('location')

        p = Paginator(room_list, 4)
        page = request.GET.get('page')
        rooms = p.get_page(page)
        return render(request, 'reservation/list_update_office.html', {'rooms': rooms})
    else:
        messages.success(request, ("You aren't authorized to do this!"))
        return redirect('some_view_name')  # Zastąp 'some_view_name' odpowiednią nazwą widoku lub URL.



@login_required
@permission_required('reservation.view_room', raise_exception=True)
def list_update_conference_room(request):
    if request.user.is_superuser:
        room_list = Room.objects.filter(destination='conference_room').order_by('location')

        p = Paginator(room_list, 4)
        page = request.GET.get('page')
        rooms = p.get_page(page)
        return render(request, 'reservation/list_update_conference_room.html', {'rooms': rooms})
    else:
        messages.success(request, ("You aren't authorized to do this!"))
        return redirect('some_view_name')  # Zastąp 'some_view_name' odpowiednią nazwą widoku lub URL.


@login_required
@permission_required('reservation.delete_room', raise_exception=True)
def delete_room(request, room_id):
    room = Room.objects.get(pk=room_id)
    if request.user.is_superuser:
        room.delete()
        messages.success(request, ("Pokój został usunięty!"))
        return redirect('list-update-room')
    else:
        messages.success(request, ("You aren't authorized to delete this room!"))
        return redirect('list-rooms')

def generate_timeline_data(reservations):
    now = datetime.now(pytz.timezone('Europe/Warsaw'))

    minutes = ((now.minute + 15) // 15) * 15
    now = now.replace(minute=minutes % 60, second=0, microsecond=0)
    if minutes == 60:
        now += timedelta(hours=1)
    current_time = now.time()

    quarter_hours = [time(hour=hour, minute=minute) for hour in range(current_time.hour, 23) for minute in [0, 15, 30, 45]]
    quarter_hours.append(time(22, 0))  # Ensure 22:00 is included in the list
    reservations = sorted([(r.start_time, r.end_time) for r in reservations])

    timeline_data = []
    i = 0
    while i < len(quarter_hours) - 1:  # Ensure we don't go beyond the end of the list
        t = quarter_hours[i]
        if any(start <= t < end or (t == start and end == time(22, 0)) for start, end in reservations):
            j = i
            while j < len(quarter_hours) - 1 and (any(start <= quarter_hours[j] < end or (quarter_hours[j] == start and end == time(22, 0)) for start, end in reservations)):
                j += 1
            timeline_data.append({
                'hour': f'{quarter_hours[i].strftime("%H:%M")}-{quarter_hours[j].strftime("%H:%M")}',
                'reserved': 'Zarezerwowane'
            })
        else:
            j = i
            while j < len(quarter_hours) - 1 and all(not(start <= quarter_hours[j] < end or (quarter_hours[j] == start and end == time(22, 0))) for start, end in reservations):
                j += 1
            if quarter_hours[i] != time(22, 0):  # Do not add "Free" for 22:00-22:00
                timeline_data.append({
                    'hour': f'{quarter_hours[i].strftime("%H:%M")}-{quarter_hours[j].strftime("%H:%M")}',
                    'reserved': 'Wolne'
                })
        i = j
    return timeline_data
