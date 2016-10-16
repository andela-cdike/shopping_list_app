from django.conf.urls import url

from app import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^shopping-list/create$',
        views.ShoppingListCreateView.as_view(), name='create-shopping-list'),
    url(r'^shopping-list/edit/(?P<id>[0-9]+)$',
        views.ShoppingListEditView.as_view(), name='edit-shopping-list'),
    url(r'^shopping-list/delete/(?P<id>[0-9]+)$',
        views.ShoppingListDeleteView.as_view(), name='delete-shopping-list'),
    url(r'^(?P<shopping_list_id>[0-9]+)/items/$',
        views.ListItemsView.as_view(), name='list-items'),
    url(r'^item/create/(?P<shopping_list_id>[0-9]+)$',
        views.ShoppingListItemCreateView.as_view(), name='create-item'),
    url(r'^item/edit/(?P<id>[0-9]+)$',
        views.ShoppingListItemEditView.as_view(), name='edit-item'),
    url(r'^item/delete/(?P<id>[0-9]+)$',
        views.ShoppingListItemDeleteView.as_view(), name='delete-item'),
    url(r'^items/search/(?P<shopping_list_id>[0-9]+)$',
        views.ShoppingListItemSearchView.as_view(), name='search-items')
]
