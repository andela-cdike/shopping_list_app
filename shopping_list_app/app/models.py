from django.db import models

from customExceptions import BudgetExceeded


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
        '''Customize save method to
        - raise exception if budget is exceeded
        - update parent shopping list balance and budget
        '''
        previous_instance = self.get_previous_instance()
        if self.price > self.shopping_list.budget and self.bought:
            raise BudgetExceeded(self)
        super(ShoppingListItem, self).save(*args, **kwargs)
        self.update_parent_shopping_list(previous_instance)
        return self

    def get_previous_instance(self):
        '''Returns the instance of self currently in database,
        otherwise, returns a dummy object if the object is just being created
        '''
        if self.id:
            return ShoppingListItem.objects.get(pk=self.id)
        return ShoppingListItem(name=self.name, price=0)

    def update_parent_shopping_list(self, previous_instance):
        '''
        Update the parent shopping list budget and balance
        '''
        self.__update_shopping_list_if_bought_field_changed(
            previous_instance.bought)
        self.__update_shopping_list_if_price_field_changed(
            previous_instance.price, previous_instance.bought)
        self.shopping_list.save()

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
