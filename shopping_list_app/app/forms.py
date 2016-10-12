from django.forms import ModelForm

from app.models import ShoppingList


class ShoppingListForm(ModelForm):
    '''Form for the shopping list model'''
    class Meta:
        model = ShoppingList
        fields = ['name']
