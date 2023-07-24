import pytest

from app_order.services.new_order import NewOrder


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def menu_item(mixer):
    return mixer.blend("app_menu.menuitem")

@pytest.fixture
def an_menu_item(mixer):
    return mixer.blend("app_menu.menuitem")

@pytest.fixture
def new_order(user):
    return NewOrder(user=user)

@pytest.fixture
def an_new_order(an_user):
    return NewOrder(user=an_user)
