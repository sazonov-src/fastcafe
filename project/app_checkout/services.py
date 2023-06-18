from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from app_checkout.models import Checkout
from app_order.services import get_new_order


def get_checkout(user: User):
    order = get_new_order(user=user)
    return Checkout.objects.get(order=order)


def update_or_create_checkout(user: User, **kwargs) -> tuple[Checkout, bool]:
    order = get_new_order(user)
    [kwargs.pop(key, None) for key in ('order', 'is_paid', 'done')]
    return Checkout.objects.update_or_create(
        order=order,
        defaults=kwargs)
