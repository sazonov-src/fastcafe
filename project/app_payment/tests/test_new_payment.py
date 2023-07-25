import pytest


pytestmark = [pytest.mark.django_db]


def test_get_url(peyment_factory):
    return print(peyment_factory.get_payment_url())
