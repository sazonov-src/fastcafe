from django.core.exceptions import ValidationError
import pytest


pytestmark = [pytest.mark.django_db]


def test_get_url(payment_error):
    assert payment_error.get_status_info()["result"] == "error"
    assert "https://" in payment_error.get_payment_url().get("url", None)


def test_payment_success(payment_ok):
    assert payment_ok.get_status_info()["result"] == "ok"
    with pytest.raises(ValidationError):
        payment_ok.get_payment_url()
    
