from django.conf.urls import url

from app import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<shopping_list_id>[0-9]+)/items/$',
        views.ListItemsView.as_view(), name='items'),
]
