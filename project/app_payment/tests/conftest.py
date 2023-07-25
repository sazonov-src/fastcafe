import pytest

from app_payment.tests.factory import PeymentFactory

pytestmark = [pytest.mark.django_db]

@pytest.fixture
def peyment_factory(user, menu_item):
    return PeymentFactory(user=user, menu_item=menu_item)
