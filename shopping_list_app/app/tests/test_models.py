from django.contrib.auth.models import User
from django.test import TestCase

from app.models import ShoppingList


class Base(TestCase):
    '''Abstracts setup'''
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'admin')
        ShoppingList.objects.create(name='Grocery', owner=user)


class ShoppingListModelTestSuite(Base):
    def test_user_model(self):
        shopping_list = ShoppingList.objects.get(name='Grocery')
        self.assertEqual(str(shopping_list), 'Grocery')
