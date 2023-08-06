from collections import namedtuple
from rest_framework.generics import get_object_or_404

from app_menu.models import MenuItem
from app_order.models import Order, OrderItem


class NewOrder:
    order_statuses = namedtuple(
        "order_statuses", ("order", "is_order_create", "item", "is_item_create"))

    def __init__(self, user) -> None:
        self._user = user

    def __call__(self):
        return get_object_or_404(Order, user=self._user, paycallback__isnull=True)

    def __getattr__(self, name):
        return getattr(self(), name)

    def update_or_create(self, item: MenuItem, quantity: int = 1):
        order = Order.objects.get_or_create(user=self._user, paycallback__isnull=True)
        order_item = OrderItem.objects.update_or_create(
            order=order[0],
            item=item,
            defaults={'quantity': int(quantity) if int(quantity) > 0 else 1})
        return self.order_statuses(*order, *order_item)

    def delete(self, order_item: OrderItem):
        if len(order_item.order.order_items) == 1:
            return order_item.order.delete()[0]
        return order_item.delete()[0]

    @property
    def orderitems_queryset(self):
        return self().orderitem_set.all()
