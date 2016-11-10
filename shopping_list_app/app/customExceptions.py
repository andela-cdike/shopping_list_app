class BudgetExceeded(Exception):
    '''
    Exception raised when user attempts to spend more than
    budget on Shopping List can support
    '''
    def __init__(self, item):
        self.shopping_list_id = item.shopping_list.id
        self.outstanding_balance = item.price - item.shopping_list.budget

    def __unicode__(self):
        return repr(self.msg)
