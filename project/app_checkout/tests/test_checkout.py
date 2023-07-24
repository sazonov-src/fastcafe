from django.core.exceptions import ValidationError
import pytest

pytestmark = [pytest.mark.django_db]


def test_default_checkout(checkout_factory):
    checkout = checkout_factory.create_new_checkout(
        user_name="Vasia",
        phone="+380-97-777-77-77")
    assert checkout_factory.order.pk == checkout.order.pk
    assert checkout.cart_pay is True
    
    
def test_not_name(checkout_factory):
    with pytest.raises(ValidationError):  
        checkout_factory.create_new_checkout(
            phone="+380-97-777-77-77")
    
    
def test_not_phone(checkout_factory):
    with pytest.raises(ValidationError):  
        checkout_factory.create_new_checkout(
            user_name="Vasia")


def test_checkout_vs_new_order(checkout_default):
    old_pk = checkout_default.order.pk
    order_obj = checkout_default.create_new_order()
    assert order_obj.order != old_pk
    assert order_obj.is_order_create is True

