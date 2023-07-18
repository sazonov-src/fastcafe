import pytest
from app_checkout.services import create_new_checkout

from app_order.services.new_order import update_or_create_new_order

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user_new_order(user, mixer):
    update_or_create_new_order(
        user=user,
        item=mixer.blend("app_menu.menuitem"))
    return user

@pytest.fixture
def user_chackout_order_cart_pay(user_new_order):
    create_new_checkout(
        user=user_new_order,
        user_name="Vasia",
        phone="+38077-777-77-77")
    return user_new_order

@pytest.fixture
def user_chackout_order_not_cart_pay(user_new_order):
    create_new_checkout(
        user=user_new_order,
        user_name="Vasia",
        phone="+38077-777-77-77",
        cart_pay=False)
    return user_new_order
