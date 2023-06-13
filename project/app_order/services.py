from django.contrib.auth.models import User

from app_menu.models import MenuItemChild
from app_order.models import Order, OrderItem


def update_or_create_order(
        user: User,
        item: MenuItemChild,
        quantity: int = 1
) -> tuple[tuple[Order, bool], tuple[OrderItem, bool]]:

    order = Order.objects.get_or_create(user=user, status='new')
    order_item = OrderItem.objects.update_or_create(
        order=order[0],
        item=item,
        defaults={'quantity': quantity})
    return order, order_item

