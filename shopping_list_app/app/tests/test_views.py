from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from app.models import ShoppingList, ShoppingListItem


class Base(TestCase):
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'admin')
        self.shopping_list = ShoppingList.objects.create(
            name='Grocery', owner=user)
        ShoppingListItem.objects.create(
            name='milk', shopping_list=self.shopping_list)
        self.client = Client()
        self.client.login(username='admin', password='admin')


class ShoppingListTestSuite(Base):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Grocery', response.content)

    def test_create_new_shopping_list(self):
        url = reverse('index')
        data = {'name': 'Grocery'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class ShoppingListItemTestSuite(Base):
    def test_view_shopping_list_items(self):
        url = reverse(
            'items', kwargs={'shopping_list_id': self.shopping_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('milk', response.content)

    def test_create_new_shopping_list_item(self):
        url = reverse(
            'items', kwargs={'shopping_list_id': self.shopping_list.id})
        data = {'name': 'sugar'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
