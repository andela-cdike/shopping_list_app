from django.db import models


class Base(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ShoppingList(Base):
    owner = models.ForeignKey(
        'auth.User', null=True, related_name='shopping_lists'
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ShoppingListItem(Base):
    shopping_list = models.ForeignKey(
        'ShoppingList', related_name='items', on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
