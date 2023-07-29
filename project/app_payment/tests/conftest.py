import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def order_checkout(checkout_default):
    return checkout_default.order


@pytest.fixture
def order_not_checkout(checkout_factory):
    order_obj = checkout_factory.create_new_order()
    return order_obj.order


@pytest.fixture
def order_error(checkout_factory):
    order_obj = checkout_factory.create_new_order()
    checkout_factory.create_new_checkout(
            user_name="Vasia",
            phone="+380984445577")    
    return order_obj.order


@pytest.fixture
def order_ok(checkout_default):
    order_obj = checkout_default.create_new_order()
    checkout_default.create_new_checkout(
        user_name="Vasia",
        phone="+380984445577")    
    return order_obj.order
