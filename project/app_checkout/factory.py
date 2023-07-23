from django.contrib.auth.models import User
from app_checkout.models import Checkout
from app_checkout.services import get_create_checkout_data

from app_menu.models import MenuItem
from app_order.services.new_order import update_or_create_new_order


class ChackoutFactory:
    def __init__(self, user: User, menu_item: MenuItem):
        self.user = user
        self.menu_item = menu_item
        self.order, self.is_created = self.create_new_order()


    def create_new_order(self):
        return update_or_create_new_order(
            user=self.user, 
            item=self.menu_item)[0] 
    
    
    def create_new_checkout(self, **kwargs):
        data=get_create_checkout_data(user=self.user, **kwargs)
        data.pop("order")
        checkout = Checkout(order=self.order, **data)
        checkout.full_clean()
        checkout.save()
        return checkout
