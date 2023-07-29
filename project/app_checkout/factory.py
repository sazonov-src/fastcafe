from django.contrib.auth.models import User
from app_checkout.models import Checkout
from app_checkout.services import NewCheckout

from app_menu.models import MenuItem


class ChackoutFactory:
    def __init__(self, user: User, menu_item: MenuItem):
        self._menu_item = menu_item
        self.checkout_serv = NewCheckout(user=user)

    @property
    def order(self):
        return self.checkout_serv.order()

     
    def create_new_checkout(self, **kwargs):
        data = self.checkout_serv.get_create_or_update_data(**kwargs)
        data.pop("order")
        checkout = Checkout(order=self.checkout_serv.order(), **data)
        checkout.full_clean()
        checkout.save()
        return checkout

    
    def create_new_order(self):
        return self.checkout_serv.order.update_or_create(item=self._menu_item)
