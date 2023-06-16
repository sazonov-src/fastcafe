from django.contrib.auth.models import User

from app_menu.models import MenuItemChild
from app_order.models import Order, OrderItem


def validate_quantity(quantity: int):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
        return quantity
    except ValueError:
        return 1


def update_or_create_order(
        user: User,
        item: MenuItemChild,
        quantity: int = 1
) -> tuple[tuple[Order, bool], tuple[OrderItem, bool]]:

    order = Order.objects.get_or_create(user=user, status='new')
    order_item = OrderItem.objects.update_or_create(
        order=order[0],
        item=item,
        defaults={'quantity': validate_quantity(quantity)})
    return order, order_item


def get_new_order(user: User):
    return Order.objects.get(user=user, status='new')


def get_new_order_items(user: User):
    return get_new_order(user).orderitem_set.all()

