from django.contrib.auth.models import User
from django.test import TestCase

from app.models import ShoppingList, ShoppingListItem


class Base(TestCase):
    '''Abstracts setup'''
    def setUp(self):
        user = User.objects.create_user('admin', 'admin@test.com', 'admin')
        self.shopping_list = ShoppingList.objects.create(
            name='Grocery', owner=user, budget=400, warning_price=50,
        )
        self.shopping_list_item = ShoppingListItem.objects.create(
            name='milk',
            shopping_list=self.shopping_list,
            price=200,
            bought=False
        )


class ShoppingListModelTestSuite(Base):
    def test_shopping_list_model(self):
        shopping_list = ShoppingList.objects.get(name='Grocery')
        self.assertEqual(str(shopping_list), 'Grocery')
        self.assertIsInstance(shopping_list.owner, User)
        self.assertEqual(type(shopping_list.budget), int)
        self.assertEqual(type(shopping_list.warning_price), int)
        self.assertEqual(type(shopping_list.balance), int)

    def test_unbought_items_balance_is_calculated_accurately(self):
        self.assertEqual(self.shopping_list.balance,
                         self.shopping_list.items.all()[0].price)
        self.shopping_list_item.bought = True
        self.shopping_list_item.save()
        self.assertEqual(self.shopping_list.balance, 0)


class ShoppingListItemModelTestSuite(Base):
    def test_shopping_list_item_model(self):
        shopping_list_item = ShoppingListItem.objects.get(name='milk')
        self.assertEqual(str(shopping_list_item), 'milk')
