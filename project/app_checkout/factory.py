from django.contrib.auth.models import User
from app_checkout.services import create_new_checkout

from app_menu.models import MenuItem
from app_order.services.new_order import update_or_create_new_order


class ChackoutFactory:
    def __init__(self, user: User, menu_item: MenuItem):
        self.user = user
        self.menu_item = menu_item
        self.order = update_or_create_new_order(
            user=self.user, 
            item=self.menu_item)[0][0] 
    
    
    def create_chackout(self, **kwargs):
        return create_new_checkout(user=self.user, **kwargs)
