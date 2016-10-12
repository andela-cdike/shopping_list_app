from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from app.models import ShoppingList


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        shopping_lists = ShoppingList.objects.filter(owner=request.user)
        context = {}
        context = {'shopping_lists': shopping_lists}
        return render(request, 'app/index.html', context)
