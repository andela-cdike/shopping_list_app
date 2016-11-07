from django.contrib.auth.models import User
from django.test import TestCase

from app.models import ShoppingList, ShoppingListItem


class Base(TestCase):
    '''Abstracts setup'''
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'admin')
        shopping_list = ShoppingList.objects.create(
            name='Grocery', owner=user, budget=400)
        ShoppingListItem.objects.create(
            name='milk', shopping_list=shopping_list, price=200, bought=False)


class ShoppingListModelTestSuite(Base):
    def test_shopping_list_model(self):
        shopping_list = ShoppingList.objects.get(name='Grocery')
        self.assertEqual(str(shopping_list), 'Grocery')
        self.assertEqual(type(shopping_list.budget), int)


class ShoppingListItemModelTestSuite(Base):
    def test_shopping_list_item_model(self):
        shopping_list_item = ShoppingListItem.objects.get(name='milk')
        self.assertEqual(str(shopping_list_item), 'milk')
