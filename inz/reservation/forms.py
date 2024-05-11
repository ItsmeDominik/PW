from datetime import time, date
import pytz
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import RoomReservation, Room, OfficeRoomReservation, Printers
from django import forms
from datetime import datetime, timedelta
from .models import PrinterRent, Company


# forms.py
class RoomReservationForm(ModelForm):
    room = forms.TextInput

    duration = forms.ChoiceField(
        choices=[
            (15, '15 minut'),
            (30, '30 minut'),
            (45, '45 minut'),
            (60, '1 godzina'),
        ],
        label='Czas Trwania',  # Polska etykieta dla tego pola
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Czas Trwania'})
    )

    start_time = forms.TimeField(
        label='Czas Rozpoczęcia',  # Polska etykieta dla tego pola
        widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM', 'type': 'time'})
        # Ustawienie typu na 'time'
    )

    def __init__(self, *args, room=None, **kwargs):
        super(RoomReservationForm, self).__init__(*args, **kwargs)

        # Set the date field to today's date
        tz = pytz.timezone('Europe/Warsaw')
        now = datetime.now(tz)
        self.initial['date'] = now.date()
        self.fields['date'].widget = forms.TextInput(attrs={'readonly': 'readonly'})  # Make date field readonly

        # Check if the current time is between 22:00 and 08:00
        if time(22, 0) <= now.time() or now.time() <= time(8, 0):
            # Disable all fields in the form
            for field in self.fields.values():
                field.disabled = True

            # Add a new attribute to the form with a message about the time restriction
            self.reservation_time_restriction = 'Rezerwacje rozpoczynamy od godziny 8:00 do 22:00.'
            return

        # Get reservations for today's date and specific room
        date = now.date()
        if room is not None:
            reservations = RoomReservation.objects.filter(date=date, room_id=room)
            self.fields['room'].initial = room.id  # Set room field

        else:
            reservations = RoomReservation.objects.filter(date=date)

        # Create a list of reserved hours
        reserved_times = [(reservation.start_time, reservation.end_time) for reservation in reservations]

        # Round the current time to the nearest quarter hour
        minutes = ((now.minute // 15) + 1) * 15
        now = now.replace(minute=minutes % 60, second=0, microsecond=0)
        if minutes == 60:
            now += timedelta(hours=1)

        # Create a list of free hours
        quarter_hours = [0, 15, 30, 45]
        free_hours = [time(hour=hour, minute=minute)
                      for hour in range(now.hour, 22)
                      for minute in quarter_hours
                      if time(hour, minute=minute) >= now.time()
                      and not any(start <= time(hour, minute=minute) < end for start, end in reserved_times)]

        # Change the start_time field to a choice field with free hours
        self.fields['start_time'] = forms.ChoiceField(
            choices=[(hour.strftime('%H:%M'), hour.strftime('%H:%M')) for hour in free_hours],
            label='Czas Rozpoczęcia',  # Dodanie etykiety
            widget=forms.Select(attrs={'class': 'form-select'})
        )
    def clean(self):
        cleaned_data = super().clean()

        # Pobierz dane z formularza
        start_time_str = cleaned_data.get('start_time')
        start_time = datetime.strptime(start_time_str, '%H:%M').time()  # Convert string to time
        duration = cleaned_data.get('duration')
        date = cleaned_data.get('date')
        room = cleaned_data.get('room')

        # Oblicz koniec rezerwacji
        end_time = (datetime.combine(date, start_time) + timedelta(minutes=int(duration))).time()

        # Pobierz istniejące rezerwacje dla tego pokoju i daty
        reservations = RoomReservation.objects.filter(date=date, room=room)

        # Sprawdź, czy nowa rezerwacja koliduje z istniejącymi rezerwacjami
        for reservation in reservations:
            if (start_time < reservation.end_time and end_time > reservation.start_time):
                raise ValidationError('Rezerwacja koliduje z istniejącą rezerwacją.')

        # Sprawdź, czy rezerwacja kończy się po godzinie 22:00
        if end_time > time(22, 0):
            raise ValidationError('Rezerwacja nie może kończyć się po godzinie 22:00.')

        return cleaned_data

    def save(self, commit=True):
        # Get the uncommitted instance
        instance = super(RoomReservationForm, self).save(commit=False)

        # Calculate the end_time based on the selected duration
        duration = timedelta(minutes=int(self.cleaned_data['duration']))
        instance.end_time = (datetime.combine(date.today(), instance.start_time) + duration).time()

        # Calculate the cost based on the selected duration and room price
        room_price = instance.room.price
        duration_multiplier = int(self.cleaned_data['duration']) / 60
        original_cost = room_price * duration_multiplier

        # Calculate discount if it's set
        discount = instance.discount or 0
        discount_amount = (original_cost * discount) / 100
        instance.cost = original_cost - discount_amount


        # Save the instance if requested
        if commit:
            instance.save()

        return instance

    class Meta:
        model = RoomReservation
        fields = ('start_time', 'duration', 'room', 'company', 'discount', 'date')
        labels = {
            'start_time': 'Czas Rozpoczęcia',
            'duration': 'Czas Trwania',
            'room': 'Sala Konferencyjna',
            'company': 'Firma',
            'discount': 'Rabat',
            'date': 'Data',
        }
        input_formats = {
            'date': ['%Y-%m-%d'],
        }
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM', 'type': 'time'}),
            'duration': forms.Select(attrs={'class': 'form-control', 'placeholder':'Czas Trwania'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Firma'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rabat'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'capacity', 'location', 'price', 'destination', 'roomImage']
        labels = {
            'name': 'Nazwa Pomieszczenia',
            'description': 'Opis',
            'capacity': 'Ilość',
            'location': 'Lokalizacja',
            'price': 'Cena',
            'destination': 'Przeznaczenie',
            'roomImage': 'Zdjęcie',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nazwa pokoju'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Opis'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Liczba miejsc'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cena'}),
        }
class OfficeRentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Pobieranie wartości user i room z przekazanych argumentów
        self.user = kwargs.pop('user', None)
        self.room = kwargs.pop('room', None)
        super(OfficeRentForm, self).__init__(*args, **kwargs)

        # Ustawianie początkowych wartości i ukrywanie pól user i room
        if self.user:
            self.fields['user'].initial = self.user
            self.fields['user'].widget = forms.HiddenInput()

        if self.room:
            self.fields['room'].initial = self.room
            self.fields['room'].widget = forms.HiddenInput()

    def save(self, commit=True):
        # Get the uncommitted instance
        instance = super(OfficeRentForm, self).save(commit=False)

        # Calculate the cost based on the difference in days and room price
        start_date = instance.start_date
        end_date = instance.end_date

        if start_date and end_date and instance.room:
            days_difference = (end_date - start_date).days
            original_cost = days_difference * instance.room.price
            print("Days Difference:", days_difference)
            print("Original Cost:", original_cost)

            # Calculate discount if it's set
            discount = instance.discount or 0
            discount_amount = (original_cost * discount) / 100
            instance.cost = original_cost - discount_amount

            print("Discount Amount:", discount_amount)
            print("Final Cost after Discount:", instance.cost)

        # Save the instance if requested
        if commit:
            instance.save()

        return instance

    class Meta:
        model = OfficeRoomReservation
        fields = ['start_date', 'end_date', 'user', 'company', 'room', 'discount' ]
        labels = {
            'start_date': 'Data Rozpoczęcia',
            'end_date': 'Data Zakończenia',
            'user': 'Użytkownik',
            'company': 'Firma',
            'room': 'Pomieszczenie',
            'discount': 'Rabat',
        }
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data rozpoczęcia'}),
            'end_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data zakończenia'}),
            'user': forms.HiddenInput(),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.HiddenInput(),
            'discount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        room = cleaned_data.get("room")

        overlapping_reservations = OfficeRoomReservation.objects.filter(
            room=room,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        if overlapping_reservations.exists():
            raise forms.ValidationError("Wybrany termin jest już zajęty. Proszę wybrać inny termin.")

        return cleaned_data


class PrinterForm(forms.ModelForm):
    date_of_last_service = forms.CharField(
        max_length=10,
        label="Data ostatniego serwisu",
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
        })
    )

    date_of_next_service = forms.CharField(
        max_length=10,
        label="Data następnego serwisu",
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
        })
    )

    def __init__(self, *args, **kwargs):
        super(PrinterForm, self).__init__(*args, **kwargs)

        # Jeśli mamy instancję (czyli aktualizujemy obiekt), ustaw wartości początkowe na podstawie instancji.
        if self.instance and self.instance.pk:
            self.initial['date_of_last_service'] = self.instance.date_of_last_service
            self.initial['date_of_next_service'] = self.instance.date_of_next_service
        else:
            today_date = date.today()
            self.initial['date_of_last_service'] = today_date.strftime('%Y-%m-%d')
            self.initial['date_of_next_service'] = (today_date + timedelta(days=180)).strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        date_of_last_service = cleaned_data.get("date_of_last_service")
        date_of_next_service = cleaned_data.get("date_of_next_service")

        if date_of_next_service and date_of_last_service:
            if date_of_next_service < date_of_last_service:
                self.add_error('date_of_next_service',
                               "Data następnego serwisu nie może być wcześniejsza niż data ostatniego serwisu.")

        return cleaned_data

    class Meta:
        model = Printers
        fields = ['model', 'serial_number', 'price', 'date_of_last_service', 'date_of_next_service', 'status']
        labels = {
            'model': 'Model:',
            'serial_number': 'Numer Seryjny',
            'status': 'Status:',
            'price': 'Cena za wydrukowanych 100 stron',
            'date_of_last_service': 'Data ostatniego serwisu',
            'date_of_next_service': 'Data następnego serwisu',
        }
        widgets = {
            'name': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cena'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '4CE0460D0G'}),
        }
        input_formats = {
            'date_of_last_service': ['%Y-%m-%d'],
            'date_of_next_service': ['%Y-%m-%d']
        }


class PrinterRentForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), label="Firma")
    printer = forms.ModelChoiceField(queryset=Printers.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}), label="Drukarka", disabled=True)

    class Meta:
        model = PrinterRent
        fields = ['printer', 'company', 'start_date', 'end_date', 'number_of_page', 'discount']
        labels = {
            'start_date': 'Data Rozpoczęcia Wynajmu:',
            'end_date': 'Data Zakończenia Wynajmu:',
            'number_of_page': 'Liczba Stron',
            'company': 'Firma',
            'printer': 'Model Drukarki',
            'discount': 'Rabat',
        }
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'number_of_page': forms.Select(attrs={'class': 'form-control'}),
            'printer': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'discount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.printer = kwargs.pop('printer', None)
        super(PrinterRentForm, self).__init__(*args, **kwargs)
        if self.printer:
            self.fields['printer'].initial = self.printer

    def save(self, commit=True):
        instance = super(PrinterRentForm, self).save(commit=False)
        instance.user = self.user
        instance.printer = self.printer
        pages_to_print = int(self.cleaned_data.get("number_of_page"))  # Konwersja liczby stron na wartość liczbową
        cost_before_discount = instance.printer.price * (pages_to_print / 100)  # Obliczenie kosztu

        # Jeśli rabat jest ustawiony, uwzględnij go w obliczeniach
        discount = self.cleaned_data.get("discount")
        if discount:
            instance.cost = cost_before_discount * (1 - discount / 100)
        else:
            instance.cost = cost_before_discount

        if commit:
            instance.save()
        return instance





