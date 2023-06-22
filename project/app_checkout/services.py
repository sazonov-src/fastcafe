from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from app_checkout.models import Checkout
from app_order.services.new_order import get_new_order


def get_checkout(user: User):
    order = get_new_order(user=user)
    return Checkout.objects.get(order=order)


def create_new_checkout(user: User, **kwargs) -> Checkout:
    order = get_new_order(user)
    [kwargs.pop(key, None) for key in ('order', 'is_paid', 'done')]
    checkout = Checkout.objects.create(order=order, **kwargs)
    order.created = True
    order.save()
    return checkout
