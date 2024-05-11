from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from company.models import Company
from events.models import Discount

class DiscountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Ustawienia początkowe dla wszystkich przypadków testowych
        test_company = Company.objects.create(companyName='Test Company')
        test_user = User.objects.create_user(username='testuser', password='password')
        Discount.objects.create(discount_title='Test Title', author=test_user, client=test_company,
                                publicationDate=date.today(), description='Test Description')
    def test_discount_title_label(self):
        discount = Discount.objects.get(id=1)
        field_label = discount._meta.get_field('discount_title').verbose_name
        self.assertEquals(field_label, 'Tytuł Rabatu')
    def test_author_label(self):
        discount = Discount.objects.get(id=1)
        field_label = discount._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Autor')
    def test_client_label(self):
        discount = Discount.objects.get(id=1)
        field_label = discount._meta.get_field('client').verbose_name
        self.assertEquals(field_label, 'Klient')
    def test_publicationDate_label(self):
        discount = Discount.objects.get(id=1)
        field_label = discount._meta.get_field('publicationDate').verbose_name
        self.assertEquals(field_label, 'Data Publikacji')
    def test_description_label(self):
        discount = Discount.objects.get(id=1)
        field_label = discount._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Opis Oferty')
    def test_discount_title_max_length(self):
        discount = Discount.objects.get(id=1)
        max_length = discount._meta.get_field('discount_title').max_length
        self.assertEquals(max_length, 256)
    def test_object_name_is_discount_title_author_client(self):
        discount = Discount.objects.get(id=1)
        expected_object_name = f'{discount.discount_title} | {discount.author.username} | {discount.client.companyName}'
        self.assertEquals(str(discount), expected_object_name)
