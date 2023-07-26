from django.core.exceptions import ValidationError
import pytest

pytestmark = [pytest.mark.django_db]


def test_default_checkout(checkout_factory):
    current_pk = checkout_factory.order.pk
    checkout = checkout_factory.create_new_checkout(
        user_name="Vasia",
        phone="+380-97-777-77-77")
    assert current_pk == checkout.order.pk
    assert checkout.cart_pay is True
    
    
def test_not_name(checkout_factory):
    with pytest.raises(ValidationError):  
        checkout_factory.create_new_checkout(
            phone="+380-97-777-77-77")
    
    
def test_not_phone(checkout_factory):
    with pytest.raises(ValidationError):  
        checkout_factory.create_new_checkout(
            user_name="Vasia")


def test_checkout_vs_new_order(checkout_factory):
    old_pk = checkout_factory.order.pk
    checkout_factory.create_new_checkout(
        user_name="Vasia",
        phone="+380-97-777-77-77")
    checkout_factory.create_new_order()
    assert checkout_factory.order.pk != old_pk

