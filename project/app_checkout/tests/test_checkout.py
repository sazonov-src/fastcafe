from django.core.exceptions import ValidationError
import pytest

pytestmark = [pytest.mark.django_db]


def test_default_checkout(checkout_factory):
    order_obj = checkout_factory.create_new_order()
    checkout = checkout_factory.create_new_checkout(
        user_name="Vasia",
        phone="+380-97-777-77-77")
    assert order_obj.order.pk == checkout.order.pk
    assert checkout.cart_pay is True
    
    
def test_not_name(checkout_factory):
    checkout_factory.create_new_order()
    with pytest.raises(ValidationError):  
        checkout_factory.create_new_checkout(
            phone="+380-97-777-77-77")
    
    
def test_not_phone(checkout_factory):
    checkout_factory.create_new_order()
    with pytest.raises(ValidationError):  
        checkout_factory.create_new_checkout(
            user_name="Vasia")


def test_checkout_vs_new_order(checkout_factory):
    order_obj = checkout_factory.create_new_order()
    checkout_factory.create_new_checkout(
        user_name="Vasia",
        phone="+380-97-777-77-77")
    new_order_obj = checkout_factory.create_new_order()
    assert order_obj.order.pk != new_order_obj.order.pk
    

