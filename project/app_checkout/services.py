from rest_framework.generics import get_object_or_404
from app_checkout.models import Checkout 
from app_order.services.new_order import NewOrder


class NewCheckout:
    def __init__(self, user):
        self._order = NewOrder(user)

    def __call__(self):
        return get_object_or_404(Checkout, order=self._order())
    
    @property
    def order(self):
        return self._order
    
    def get_create_or_update_data(self, **data):
        return data | dict(order=self._order().pk)
