import pytest


pytestmark = [pytest.mark.django_db]


def test_get_url(payment_error):
    assert payment_error.get_status_info()["result"] == "error"
    assert "https://" in payment_error.get_payment_url().get("url", None)


def test_payment_success(payment_success):
    assert payment_success.get_status_info()["result"] == "ok"
    assert "https://" in payment_success.get_payment_url().get("url", None)
    
