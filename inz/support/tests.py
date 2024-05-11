from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from .models import Ticket, Room  # Zaimportuj modele

class TicketModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Ustal testowe dane
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
        Ticket.objects.create(
            title='Test Title',
            description='Test Description',
            status='new',
            category='software',
            priority='low',
            room=test_room,
            user=test_user,
            end_time=timezone.now() + timedelta(days=1)
        )
    def test_ticket_attributes(self):
        # Pobierz obiekt zgłoszenia
        ticket = Ticket.objects.get(id=1)
        # Sprawdź atrybuty zgłoszenia
        self.assertEquals(ticket.title, 'Test Title')
        self.assertEquals(ticket.description, 'Test Description')
        self.assertEquals(ticket.status, 'new')
        self.assertEquals(ticket.category, 'software')
        self.assertEquals(ticket.priority, 'low')
        self.assertEquals(ticket.room.name, 'Test Room')  # Upewnij się, że relacja ForeignKey działa
        self.assertEquals(ticket.user.username, 'testuser')  # Upewnij się, że relacja ForeignKey działa
        # Upewnij się, że pole `creation_time` zostało automatycznie ustawione
        self.assertIsNotNone(ticket.creation_time)
        # Upewnij się, że pole `end_time` jest prawidłowe
        expected_end_time = timezone.now() + timedelta(days=1)
        self.assertAlmostEqual(ticket.end_time, expected_end_time, delta=timedelta(seconds=1))
