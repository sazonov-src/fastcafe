import pytest

pytestmark = [pytest.mark.django_db]


def test_default_checkout(checkout_factory):
    checkout = checkout_factory.create_new_checkout(
        user_name="Vasia",
        phone="+380-97-777-77-77")
    assert checkout_factory.order.pk == checkout.order.pk
    assert checkout.cart_pay is True
    
    
