from django.forms import ModelForm

from app.models import ShoppingList, ShoppingListItem


class ShoppingListForm(ModelForm):
    '''Form for the shopping list model'''
    class Meta:
        model = ShoppingList
        fields = ['name']


class ShoppingListItemForm(ModelForm):
    '''Form for the shopping list model'''
    class Meta:
        model = ShoppingListItem
        fields = ['name']
