from django.contrib.auth.models import User
from django.test import TestCase

from app.models import ShoppingList, ShoppingListItem


class Base(TestCase):
    '''Abstracts setup'''
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'admin')
        shopping_list = ShoppingList.objects.create(
            name='Grocery', owner=user)
        ShoppingListItem.objects.create(
            name='milk', shopping_list=shopping_list)


class ShoppingListModelTestSuite(Base):
    def test_user_model(self):
        shopping_list = ShoppingList.objects.get(name='Grocery')
        self.assertEqual(str(shopping_list), 'Grocery')


class ShoppingListItemModelTestSuite(Base):
    def test_user_model(self):
        shopping_list = ShoppingList.objects.get(name='milk')
        self.assertEqual(str(shopping_list), 'milk')
