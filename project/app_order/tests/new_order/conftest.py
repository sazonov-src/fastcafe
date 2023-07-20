import pytest

from app_order.services.new_order import update_or_create_new_order

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def menu_item(mixer):
    return mixer.blend("app_menu.menuitem")

@pytest.fixture
def an_menu_item(mixer):
    return mixer.blend("app_menu.menuitem")

@pytest.fixture
def order_with_one_item(menu_item, user):
    order = update_or_create_new_order(user=user, item=menu_item)[0][0]
    return order

@pytest.fixture
def order_with_two_items(menu_item, an_menu_item, user):
    update_or_create_new_order(user=user, item=menu_item)[0][0]
    order = update_or_create_new_order(user=user, item=an_menu_item)[0][0]
    return order
