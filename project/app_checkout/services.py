from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from app_checkout.models import Checkout
from app_order.services.manager import get_in_process_orders_queryset
from app_order.services.new_order import get_new_order


def get_new_checkout(user: User) -> Checkout:
    order = get_new_order(user=user)
    return get_object_or_404(Checkout, order=order)


def get_create_checkout_data(user: User, **data):
    order_pk = get_new_order(user).pk
    return data | dict(order=order_pk)


def get_manage_checkout(order_pk: int) -> Checkout:
    order = get_object_or_404(
        get_in_process_orders_queryset().filter(pk=order_pk))
    return order.checkout
