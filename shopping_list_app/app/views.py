from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, render
from django.template.context_processors import csrf
from django.urls import reverse
from django.views.generic import View


from app.forms import ShoppingListForm, ShoppingListItemForm
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
            for key in form.errors:
                for error in form.errors[key]:
                    messages.add_message(request, messages.INFO, error)

            shopping_lists = ShoppingList.objects.filter(owner=request.user)
            context = {}
            context.update(csrf(request))
            context.update({'shopping_lists': shopping_lists, 'form': form})
            return render(request, 'app/index.html', context)


class ListItemsView(LoginRequiredMixin, View):
    '''View for listing and creating new items in a shopping list'''
    def get(self, request, *args, **kwargs):
        '''Handles get requests to view

        Args:
            shopping_list_id -- id of the parent shopping list
        '''
        shopping_list_id = kwargs.get('shopping_list_id')
        shopping_list = ShoppingList.objects.get(pk=shopping_list_id)
        items = ShoppingListItem.objects.filter(shopping_list=shopping_list)

        form = ShoppingListItemForm()
        context = {}
        context.update(csrf(request))
        context.update({
            'shopping_list': shopping_list,
            'items': items,
            'form': form
        })
        return render(request, 'app/items.html', context)

    def post(self, request, *args, **kwargs):
        '''Handles post requests to view

        Args:
            shopping_list_id -- id of the parent shopping list
        '''
        form = ShoppingListItemForm(data=request.POST)
        shopping_list_id = kwargs.get('shopping_list_id')
        shopping_list = ShoppingList.objects.get(pk=shopping_list_id)

        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.shopping_list = shopping_list
            new_item.save()
            return HttpResponseRedirect(
                reverse('items',
                        kwargs={'shopping_list_id': shopping_list_id})
            )

        else:
            for key in form.errors:
                for error in form.errors[key]:
                    messages.add_message(request, messages.INFO, error)

            items = ShoppingListItem.objects.filter(
                shopping_list=shopping_list)
            context = {}
            context.update(csrf(request))
            context.update({
                'shopping_list': shopping_list,
                'items': items,
                'form': form
            })
            return render(request, 'app/items.html', context)


class ItemRenameView(View):
    '''View for renaming a shopping list item'''

    def get(self, request, *args, **kwargs):
        '''Returns a form to the user where item can be renamed'''
        id = kwargs.get('id')
        item = ShoppingListItem.objects.get(pk=id)
        form = ShoppingListItemForm(instance=item)
        context = {}
        context.update(csrf(request))
        context.update({'form': form, 'id': id})
        return render(request, 'app/edit-item.html', context)

    def post(self, request, *args, **kwargs):
        '''Handles post requests to view

        Args:
            id -- item id
        '''
        id = kwargs.get('id')
        item = ShoppingListItem.objects.get(pk=id)
        form = ShoppingListItemForm(data=request.POST)

        if form.is_valid():
            item.name = form.data['name']
            item.save()
            return HttpResponseRedirect(
                reverse('items',
                        kwargs={'shopping_list_id': item.shopping_list.id})
            )

        else:
            for key in form.errors:
                for error in form.errors[key]:
                    messages.add_message(request, messages.INFO, error)

            context = {}
            context.update(csrf(request))
            context.updat({
                'form': form
            })
        return render(request, 'app/edit-item.html', context)


class ItemDeleteView(View):
    '''View for renaming a shopping list item'''
    def get(self, request, *args, **kwargs):
        '''Returns a form to user to confirm delete'''
        id = kwargs.get('id')
        item = ShoppingListItem.objects.get(pk=id)
        context = {}
        context.update(csrf(request))
        context.update({'item': item})
        return render(request, 'app/delete-item.html', context)

    def post(self, request, *args, **kwargs):
        '''Handles post requests to view

        Args:
            id -- item id
        '''
        id = kwargs.get('id')
        item = ShoppingListItem.objects.get(pk=id)
        item.delete()
        return HttpResponseRedirect(
            reverse('items',
                    kwargs={'shopping_list_id': item.shopping_list.id})
        )
