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
    budget = models.IntegerField()
    warning_price = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ShoppingListItem(Base):
    shopping_list = models.ForeignKey(
        'ShoppingList', related_name='items', on_delete=models.CASCADE
    )
    price = models.IntegerField()
    bought = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''Update parent shopping list if item gets bought'''
        super(ShoppingListItem, self).save(*args, **kwargs)
        if self.bought:
            self.shopping_list.budget -= self.price
            self.shopping_list.save()
        return self
