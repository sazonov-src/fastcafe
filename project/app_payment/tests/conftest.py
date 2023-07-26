import pytest

from app_payment.tests.factory import PeymentFactory

pytestmark = [pytest.mark.django_db]

@pytest.fixture
def payment_factory(user, menu_item):
    return PeymentFactory(user=user, menu_item=menu_item)

@pytest.fixture
def payment_error(payment_factory):
    return payment_factory

@pytest.fixture
def payment_success(payment_factory):
    payment_factory.checkout()
    return payment_factory
