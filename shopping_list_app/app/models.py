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
    balance = models.IntegerField(default=0)

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
        '''Update parent shopping list balance and budget'''
        if self.id:
            previous_instance = ShoppingListItem.objects.get(pk=self.id)
        else:
            previous_instance = ShoppingListItem(name=self.name, price=0)
        super(ShoppingListItem, self).save(*args, **kwargs)
        self.__update_shopping_list_if_bought_field_changed(
            previous_instance.bought)
        self.__update_shopping_list_if_price_field_changed(
            previous_instance.price, previous_instance.bought)
        self.shopping_list.save()
        return self

    def __update_shopping_list_if_bought_field_changed(
        self, previous_bought=False
    ):
        '''
        Update shopping list's budget and balance fields appropriately when
        shopping list item bought field changes
        '''
        if self.bought > previous_bought:
            self.shopping_list.budget -= self.price
            self.shopping_list.balance -= self.price
        elif self.bought < previous_bought:
            self.shopping_list.budget += self.price
            self.shopping_list.balance += self.price

    def __update_shopping_list_if_price_field_changed(
            self, previous_price=0, previous_bought=False
    ):
        '''
        Update shopping list's budget and balance fields appropriately when
        shopping list item price field changes
        '''
        diff = self.price - previous_price
        self.shopping_list.balance += diff
        if self.bought != previous_bought:
            self.shopping_list.budget += diff
