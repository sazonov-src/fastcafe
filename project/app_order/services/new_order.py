from collections import namedtuple
from django.contrib.auth.models import User

from app_menu.models import MenuItem
from app_order.models import Order, OrderItem


class NewOrder:
    order_statuses = namedtuple(
        "order_statuses", ("order", "is_order_create", "item", "is_item_create"))
    
    
    def __init__(self, user: User) -> None:
        self._user = user
    
       
    def __call__(self):
        return Order.objects.get(user=self._user, checkout__isnull=True)
    

    def __getattr__(self, name):
        return getattr(self(), name)
    
    
    def update_or_create(self, item: MenuItem, quantity: int = 1):
        order = Order.objects.get_or_create(user=self._user, checkout__isnull=True) 
        order_item = OrderItem.objects.update_or_create(
            order=order[0],
            item=item,
            defaults={'quantity': int(quantity) if int(quantity) > 0 else 1})
        return self.order_statuses(*order, *order_item)            

    
    def delete(self, item: MenuItem) -> None:
        order_items = self().orderitem_set.all()
        order_item = order_items.get(item=item)
        if len(order_items) == 1:
            return order_item.order.delete()[0]
        return order_item.delete()[0]


    @property
    def orderitems_queryset(self):
        return self().orderitem_set.all()

    

