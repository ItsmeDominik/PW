from datetime import date
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Room, OfficeRoomReservation, Company  # Zaimportuj modele
class OfficeRoomReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Ustal testowe dane
        test_company = Company.objects.create(
            companyName='Test Company',
            zipCode='00-000',
            location='Test Location',
            nip='1234567890',
            businessArea='it'
        )
        test_user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        test_room = Room.objects.create(
            name='Test Room',
            description='Test Description',
            capacity=10,
            price=100,
            destination='office',
            location='I'
        )
        OfficeRoomReservation.objects.create(
            start_date=date(2022, 1, 1),
            end_date=date(2022, 1, 2),
            user=test_user,
            company=test_company,
            room=test_room,
            cost=200
        )
    def test_office_room_reservation(self):
        # Pobierz obiekt rezerwacji
        reservation = OfficeRoomReservation.objects.get(id=1)
        # Sprawdź, czy data startowa jest prawidłowa
        self.assertEquals(reservation.start_date, date(2022, 1, 1))

