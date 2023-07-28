import pytest

from app_payment.services import NewPayment


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def payment_checkout(checkout_default):
    return NewPayment(checkout_default.order)


@pytest.fixture
def payment_not_checkout(checkout_factory):
    return NewPayment(checkout_factory.order)


@pytest.fixture
def payment_error(checkout_factory):
    order_obj = checkout_factory.create_new_order()
    checkout_factory.create_new_checkout(
            user_name="Vasia",
            phone="+380984445577")    
    return NewPayment(order_obj.order)



@pytest.fixture
def payment_ok(checkout_default):
    order_obj = checkout_default.create_new_order()
    checkout_default.create_new_checkout(
        user_name="Vasia",
        phone="+380984445577")    
    return NewPayment(order_obj.order)
