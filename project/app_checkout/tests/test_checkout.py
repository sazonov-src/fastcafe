import pytest

from app_checkout.services import create_new_checkout
from app_order.services.new_order import get_new_order, update_or_create_new_order

pytestmark = [pytest.mark.django_db]

def test_default_checkout(checkout_factory):
    checkout = checkout_factory.create_chackout(
        user_name="Vasia",
        phone="+38077-777-77-77")
    assert checkout_factory.order.pk == checkout.order.pk
    assert checkout.cart_pay is True
    
    
    
def test_default_checkout_not_name(checkout_factory):
    checkout = checkout_factory.create_chackout(
        phone="+38077-777-77-77")
    assert checkout_factory.order.pk == checkout.order.pk
    assert checkout.cart_pay is True
    
    
def test_default_checkout_not_phone(checkout_factory):
    checkout = checkout_factory.create_chackout()
    assert checkout_factory.order.pk == checkout.order.pk
    assert checkout.cart_pay is True
    
