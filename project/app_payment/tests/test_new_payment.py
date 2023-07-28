from django.core.exceptions import ValidationError
import pytest

from app_payment.services import AlreadyPayedValidationError, NewPayment, NoCheckoutValidationError


pytestmark = [pytest.mark.django_db]


def test_get_url(order_error):
    payment_error = NewPayment(order_error)
    assert payment_error.get_status_info()["result"] == "error"
    assert "https://" in payment_error.get_payment_url().get("url", "")


def test_payment_success(order_ok):
    payment_ok = NewPayment(order_ok)
    assert payment_ok.get_status_info()["result"] == "ok"
    with pytest.raises(AlreadyPayedValidationError):
        payment_ok.get_payment_url()
    

def test_payment_not_checkout(order_not_checkout):
    with pytest.raises(NoCheckoutValidationError):
        NewPayment(order_not_checkout)


def test_payment_num(order_ok):
    NewPayment(order_ok.pk)


def test_payment_not_num(num="d"):
    with pytest.raises(ValidationError):
        NewPayment(num)
    
