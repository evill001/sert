from django.test import TestCase, Client
from django.contrib.auth.models import User
from certification_app.models import Document

class WebAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_page_availability(self):
        """Проверка доступности страниц"""
        urls = ['/', '/profile/', '/services/', '/contact/', '/onas/']
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f'Страница {url} недоступна')

    def test_document_creation(self):
        """Тест создания документа"""
        document = Document.objects.create(user=self.user, title='Тестовый документ', description='Описание', status='created', price=100.00)
        self.assertEqual(Document.objects.count(), 1)
        self.assertEqual(document.title, 'Тестовый документ')

    def test_balance_update(self):
        """Тест пополнения баланса"""
        self.user.profile.balance = 100.00
        self.user.profile.save()
        self.assertEqual(self.user.profile.balance, 100.00)