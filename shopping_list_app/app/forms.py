from django import forms

from app.models import ShoppingList, ShoppingListItem


class ShoppingListForm(forms.ModelForm):
    '''Form for the shopping list model'''
    class Meta:
        model = ShoppingList
        fields = ['name', 'budget']


class ShoppingListItemForm(forms.ModelForm):
    '''Form for the shopping list model'''
    class Meta:
        model = ShoppingListItem
        fields = ['name', 'price', 'bought']
