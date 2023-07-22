from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from app_menu.models import MenuItem
from app_order.models import Order, OrderItem


def validate_quantity(quantity: int):
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
        return quantity
    except ValueError:
        return 1


def update_or_create_new_order(
        user: User,
        item: MenuItem,
        quantity: int = 1
) -> tuple[tuple[Order, bool], tuple[OrderItem, bool]]:

    order = Order.objects.get_or_create(user=user, checkout__isnull=True) 
    order_item = OrderItem.objects.update_or_create(
        order=order[0],
        item=item,
        defaults={'quantity': validate_quantity(quantity)})
    return order, order_item


def delete_new_order_item(order_item: OrderItem) -> None:
    order = order_item.order
    if len(order.order_items) == 1:
        return order.delete()
    order_item.delete()


def get_new_order(user: User) -> Order:
    return get_object_or_404(Order, user=user.pk)


def get_new_orderitems_queryset(user: User):
    return get_new_order(user).orderitem_set.all()


