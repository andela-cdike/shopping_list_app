from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, render
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView


from app.forms import ShoppingListForm, ShoppingListItemForm
from app.models import ShoppingList, ShoppingListItem


class IndexView(LoginRequiredMixin, ListView):
    model = ShoppingList
    template_name = 'app/index.html'
    context_object_name = 'shopping_lists'

    def get_context_data(self, **kwargs):
        context = super(
            IndexView, self).get_context_data(**kwargs)
        context['form'] = ShoppingListForm()
        return context


class ShoppingListCreateView(LoginRequiredMixin, CreateView):
    model = ShoppingList
    template_name = 'app/index.html'
    success_url = reverse_lazy('index')
    form_class = ShoppingListForm

    def form_valid(self, form):
        '''if valid, make the current user the owner of this shopping list'''
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        return super(ShoppingListCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(
            ShoppingListCreateView, self).get_context_data(**kwargs)
        context['shopping_lists'] = ShoppingList.objects.filter(
            owner=self.request.user)
        return context


class ShoppingListEditView(LoginRequiredMixin, UpdateView):
    '''View for editing a shopping list'''
    context_object_name = 'item'
    model = ShoppingList
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'
    template_name = 'app/edit-item.html'
    form_class = ShoppingListForm

    def get_context_data(self, **kwargs):
        context = super(
            ShoppingListEditView, self).get_context_data(**kwargs)
        context['url_name'] = 'edit-shopping-list'
        return context


class ShoppingListDeleteView(DeleteView):
    '''View for renaming a shopping list'''
    model = ShoppingList
    success_url = reverse_lazy('index')
    pk_url_kwarg = 'id'
    template_name = 'app/delete-item.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(
            ShoppingListDeleteView, self).get_context_data(**kwargs)
        context['url_name'] = 'delete-shopping-list'
        return context


class ListItemsView(LoginRequiredMixin, ListView):
    model = ShoppingListItem
    template_name = 'app/items.html'
    context_object_name = 'items'

    def get_queryset(self):
        '''Return items in the shopping list calling this view'''
        queryset = super(
            ListItemsView, self).get_queryset()
        shopping_list_id = self.kwargs['shopping_list_id']
        queryset = queryset.filter(shopping_list=shopping_list_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            ListItemsView, self).get_context_data(**kwargs)
        shopping_list_id = self.kwargs['shopping_list_id']
        context['form'] = ShoppingListItemForm()
        context['shopping_list'] = ShoppingList.objects.get(
            pk=shopping_list_id)
        return context


class ShoppingListItemCreateView(LoginRequiredMixin, CreateView):
    model = ShoppingListItem
    template_name = 'app/items.html'
    form_class = ShoppingListItemForm

    def get_success_url(self):
        return reverse(
            'list-items',
            kwargs={'shopping_list_id': self.kwargs['shopping_list_id']}
        )

    def form_valid(self, form):
        '''if valid, make the current user the owner of this shopping list'''
        self.object = form.save(commit=False)
        shopping_list_id = self.kwargs['shopping_list_id']
        shopping_list = ShoppingList.objects.get(pk=shopping_list_id)
        self.object.shopping_list = shopping_list
        return super(ShoppingListItemCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        '''Add parent shopping list to context'''
        context = super(
            ShoppingListItemCreateView, self).get_context_data(**kwargs)
        shopping_list_id = self.kwargs['shopping_list_id']
        context['items'] = ShoppingListItem.objects.filter(
            shopping_list=shopping_list_id)
        context['shopping_list'] = ShoppingList.objects.get(
            pk=shopping_list_id)
        return context

class ShoppingListItemEditView(LoginRequiredMixin, UpdateView):
    '''View for editing a shopping list item'''
    context_object_name = 'item'
    model = ShoppingListItem
    pk_url_kwarg = 'id'
    template_name = 'app/edit-item.html'
    form_class = ShoppingListItemForm

    def get_success_url(self):
        item = ShoppingListItem.objects.get(pk=self.kwargs['id'])
        return reverse(
            'list-items',
            kwargs={'shopping_list_id': item.shopping_list.id}
        )

    def get_context_data(self, **kwargs):
        context = super(
            ShoppingListItemEditView, self).get_context_data(**kwargs)
        context['url_name'] = 'edit-item'
        return context


class ShoppingListItemDeleteView(LoginRequiredMixin, DeleteView):
    '''View for renaming a shopping list item'''
    context_object_name = 'item'
    model = ShoppingListItem
    pk_url_kwarg = 'id'
    template_name = 'app/delete-item.html'

    def get_success_url(self):
        item = ShoppingListItem.objects.get(pk=self.kwargs['id'])
        return reverse(
            'list-items',
            kwargs={'shopping_list_id': item.shopping_list.id}
        )

    def get_context_data(self, **kwargs):
        context = super(
            ShoppingListItemDeleteView, self).get_context_data(**kwargs)
        context['url_name'] = 'delete-item'
        return context
