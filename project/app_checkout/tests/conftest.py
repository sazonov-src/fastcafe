import pytest

from app_checkout.factory import ChackoutFactory 

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def checkout_factory(user, menu_item):
    return ChackoutFactory(user=user, menu_item=menu_item)


@pytest.fixture
def checkout_default(checkout_factory):
    checkout_factory.create_new_checkout(
        user_name="Vasia",
        phone="+380-97-777-77-77")
    return checkout_factory

