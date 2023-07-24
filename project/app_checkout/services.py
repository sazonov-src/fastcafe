from app_checkout.models import Checkout as ch
from app_order.services.new_order import NewOrder


class NewCheckout:
    def __init__(self, user):
        self._order = NewOrder(user)

    
    def __call__(self):
        return ch.objects.get(order=self._order())

    
    def __getattr__(self, name):
        return getattr(self(), name)


    @property
    def order(self):
        return self._order

    
    def get_create_or_update_data(self, **data):
        return data | dict(order=self._order().pk)
