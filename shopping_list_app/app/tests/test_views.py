from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from app.models import ShoppingList, ShoppingListItem


class Base(TestCase):
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'admin')
        self.shopping_list = ShoppingList.objects.create(
            name='Grocery',
            owner=user,
            budget=400,
            warning_price=50,
        )
        self.item = ShoppingListItem.objects.create(
            name='milk',
            shopping_list=self.shopping_list,
            price=50,
            bought=False
        )
        self.client = Client()
        self.client.login(username='admin', password='admin')


class ShoppingListTestSuite(Base):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Grocery', response.content)

    def test_create_new_shopping_list(self):
        url = reverse('create-shopping-list')
        data = {'name': 'Grocery', 'budget': 400, 'warning_price': 100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_edit_shopping_list_route(self):
        url = reverse(
            'edit-shopping-list', kwargs={'id': self.shopping_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_shopping_list(self):
        url = reverse(
            'edit-shopping-list', kwargs={'id': self.shopping_list.id})
        data = {'name': 'Luxury', 'budget': 20000000, 'warning_price': 1000000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        item = ShoppingList.objects.get(pk=self.shopping_list.id)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.budget, data['budget'])

    def test_delete_shopping_list_route(self):
        url = reverse(
            'delete-shopping-list', kwargs={'id': self.shopping_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_shopping_list(self):
        url = reverse(
            'delete-shopping-list', kwargs={'id': self.shopping_list.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRaises(
            ShoppingList.DoesNotExist,
            ShoppingList.objects.get,
            pk=self.shopping_list.id
        )

    def test_warning_is_not_displayed_if_warning_price_is_not_reached(self):
        url = reverse(
            'list-items', kwargs={'shopping_list_id': self.shopping_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('You are running out of cash.', response.content)

    def test_warn_user_if_shopping_list_warning_price_is_reached(self):
        self.shopping_list.budget = 45
        self.shopping_list.save()
        url = reverse(
            'list-items', kwargs={'shopping_list_id': self.shopping_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('You are running out of cash.', response.content)


class ShoppingListItemTestSuite(Base):
    def test_view_shopping_list_items(self):
        url = reverse(
            'list-items', kwargs={'shopping_list_id': self.shopping_list.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.item.name.capitalize(), response.content)
        self.assertIn(str(self.item.price), response.content)

    def test_create_new_shopping_list_item(self):
        url = reverse(
            'create-item', kwargs={'shopping_list_id': self.shopping_list.id})
        data = {'name': 'sugar', 'price': 20, 'bought': False}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_edit_shopping_list_item_route(self):
        url = reverse(
            'edit-item', kwargs={'id': self.item.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_shopping_list_item(self):
        url = reverse(
            'edit-item', kwargs={'id': self.item.id}
        )
        data = {'name': 'Sugar', 'price': 330, 'bought': True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        item = ShoppingListItem.objects.get(pk=self.item.id)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.price, data['price'])
        self.assertEqual(item.bought, data['bought'])

    def test_delete_shopping_list_item_route(self):
        url = reverse(
            'delete-item', kwargs={'id': self.item.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_shopping_list_item_name(self):
        url = reverse(
            'delete-item', kwargs={'id': self.item.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
