from django.db import models
from django.contrib.auth.models import User
from company.models import Company
from datetime import date, timedelta
from datetime import date

class Room(models.Model):
    # Definicja dostępnych wyborów dla lokalizacji (piętro) i przeznaczenia pomieszczenia
    LOCATIONS_CHOICES = [
        ('I', 'Piętro I'),
        ('II', 'Piętro II'),
        ('III', 'Piętro III'),
        ('IV', 'Piętro IV'),
        ('V', 'Piętro V'),
        ('VI', 'Piętro VI'),
        ('VII', 'Piętro VII'),
    ]
    ROOM_DESTINATION = [
        ('office', 'Biuro'),
        ('conference_room', 'Sala Konferencyjna'),
    ]
    # Pole na nazwę pomieszczenia, z ograniczeniem do 200 znaków
    name = models.CharField('Nazwa', max_length=200)
    # Pole tekstowe na opis pomieszczenia
    description = models.TextField('Opis')
    # Liczba całkowita opisująca pojemność pomieszczenia
    capacity = models.IntegerField('Ilość Osób')
    # Liczba całkowita opisująca cenę wynajmu
    price = models.IntegerField("Cena")
    # Wybór przeznaczenia pomieszczenia z predefiniowanych opcji
    destination = models.CharField(
        'Przeznaczenie',
        max_length=32,
        choices=ROOM_DESTINATION,
        default='office',  # Domyślna wartość
     )
    # Wybór piętra, na którym znajduje się pomieszczenie, z predefiniowanych opcji
    location = models.CharField(
        'Piętro',
        max_length=32,
        choices=LOCATIONS_CHOICES,
        default='I',  # Domyślna wartość
     )
    # Pole na zdjęcie pomieszczenia, opcjonalne
    roomImage = models.ImageField('Zdjęcie', null=True, blank=True, upload_to='images')
    # Metoda zwracająca czytelną reprezentację modelu
    def __str__(self):
        return self.name
    # Dodatkowe metadane dla modelu
    class Meta:
        verbose_name = 'Pomieszczenia'
        verbose_name_plural = 'Pomieszczenia'



class OfficeRoomReservation(models.Model):
    # Pole na datę rozpoczęcia rezerwacji
    start_date = models.DateField('Data rozpoczęcia')

    # Pole na datę zakończenia rezerwacji
    end_date = models.DateField('Data zakończenia')

    # Klucz obcy do modelu użytkownika; relacja nie może być pusta (CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")

    # Klucz obcy do modelu firmy; relacja nie może być pusta (CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Firma")

    # Klucz obcy do modelu pomieszczenia; relacja nie może być pusta (CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pomieszczenie")

    # Liczba całkowita opisująca koszt rezerwacji
    cost = models.IntegerField("Koszt")

    # Liczba całkowita opisująca rabat; opcjonalne
    discount = models.IntegerField("Rabat", blank=True, null=True)

    # Metoda zwracająca czytelną reprezentację modelu
    def __str__(self):
        return f"{self.user.first_name} | {self.user.last_name} | {self.company} | {self.room}"

    # Dodatkowe metadane dla modelu
    class Meta:
        verbose_name = 'Biura'
        verbose_name_plural = 'Biura'

class RoomReservation(models.Model):
    date = models.DateField('Data')
    start_time = models.TimeField('Data Rozpoczęcia')
    end_time = models.TimeField('Data Zakończenia')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Firma")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Pomieszczenie")
    cost = models.IntegerField("Koszt")
    discount = models.IntegerField("Rabat", blank=True, null=True)
    def __str__(self):
        return f"{self.user.first_name} | {self.user.last_name} | {self.company} | {self.date}"
    class Meta:
        verbose_name = 'Sale Konferencyjne'
        verbose_name_plural = 'Sale Konferencyjne'

class Printers(models.Model):
    price = models.IntegerField("Cena")
    serial_number = models.CharField('Numer Seryjny', max_length=200)
    date_of_last_service = models.DateField('Data Ostatniego Serwisu', null=True)
    date_of_next_service = models.DateField('Data Następnego Serwisu', null=True)
    PRINTER_STATUS = [
        ('in_use', 'W Użyciu'),
        ('service', 'Na Serwisie'),
        ('unused', 'Nie używana'),
    ]
    status = models.CharField(
        'Status',
        max_length=32,
        choices=PRINTER_STATUS,
        default='unused'
    )
    PRINTER_MODEL_CHOICES = [
        ('HP_LaserJet', 'HP LaserJet Pro M404n'),
        ('Canon_PIXMA', 'Canon PIXMA TR4520'),
        ('Epson_WorkForce', 'Epson WorkForce WF-2830'),
        ('Brother_HL', 'Brother HL-L2300D'),
        ('Samsung_M2020', 'Samsung Xpress M2020W'),
        ('Lexmark_C3224', 'Lexmark C3224dw'),
        ('Dell_E310', 'Dell E310DW'),
    ]
    model = models.CharField(
        'Model',
        max_length=32,
        choices=PRINTER_MODEL_CHOICES,
        default='HP_LaserJet'
    )
    def __str__(self):
        return f"{self.get_model_display()}"
    class Meta:
        verbose_name = 'Drukarki'
        verbose_name_plural = 'Drukarki'

class PrinterRent(models.Model):
    start_date = models.DateField('Data rozpoczęcia', default=date.today)
    end_date = models.DateField('Data zakończenia')
    NUMBER_OF_PAGE_CHOICES = [
        ('100', '100'),
        ('250', '250'),
        ('500', '500'),
        ('1000+', '1000+'),
    ]
    number_of_page = models.CharField(
        'Liczba stron',
        max_length=32,
        choices=NUMBER_OF_PAGE_CHOICES,
        default='100'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Użytkownik")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Firma")
    printer = models.ForeignKey(Printers, on_delete=models.CASCADE, verbose_name="Drukarka")
    cost = models.IntegerField("Koszt")
    discount = models.IntegerField("Rabat", blank=True, null=True)
    def __str__(self):
        return f"{self.printer.model} | {self.start_date} | {self.company.companyName} | {self.cost}"
    class Meta:
        verbose_name = 'Wynajem Drukarek'
        verbose_name_plural = 'Wynajem Drukarek'
