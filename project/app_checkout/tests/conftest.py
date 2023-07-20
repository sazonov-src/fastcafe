import pytest

from app_checkout.factory import ChackoutFactory 

pytestmark = [pytest.mark.django_db]

@pytest.fixture
def checkout_factory(user, menu_item):
    return ChackoutFactory(user=user, menu_item=menu_item)
