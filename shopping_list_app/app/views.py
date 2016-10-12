from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, render
from django.template.context_processors import csrf
from django.urls import reverse
from django.views.generic import View


from app.forms import ShoppingListForm
from app.models import ShoppingList, ShoppingListItem


class IndexView(LoginRequiredMixin, View):
    '''View for listing and creating a new shopping list'''
    def get(self, request):
        form = ShoppingListForm()
        shopping_lists = ShoppingList.objects.filter(owner=request.user)
        context = {}
        context.update(csrf(request))
        context.update({'shopping_lists': shopping_lists, 'form': form})
        return render(request, 'app/index.html', context)

    def post(self, request):
        form = ShoppingListForm(data=request.POST)

        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.owner = request.user
            new_list.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            shopping_lists = ShoppingList.objects.filter(owner=request.user)
            context = {}
            context.update(csrf(request))
            context.update({'shopping_lists': shopping_lists, 'form': form})
            return render(request, 'app/index.html', context)


class ListItemsView(LoginRequiredMixin, View):
    '''View for listing and creating new items in a shopping list'''
    def get(self, request, *args, **kwargs):
        shopping_list_id = kwargs.get('shopping_list_id')
        shopping_list = ShoppingList.objects.get(id=shopping_list_id)
        items = ShoppingListItem.objects.filter(shopping_list=shopping_list)
        context = {}
        context.update({
            'shopping_list': shopping_list,
            'items': items
        })
        return render(request, 'app/items.html', context)

