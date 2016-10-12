from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from app.models import ShoppingList


class Base(TestCase):
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'admin')
        ShoppingList.objects.create(name='Grocery', owner=user)
        self.client = Client()
        self.client.login(username='admin', password='admin')


class ShoppingListTestSuite(Base):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Grocery', response.content)
