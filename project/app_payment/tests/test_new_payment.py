from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
import pytest

from app_payment.services import AlreadyPayedValidationError, NoCheckoutValidationError
from app_payment.tests.conftest import TstNewPayment


pytestmark = [pytest.mark.django_db]


def test_payment_ok(order_ok, order_ok_callback):
    payment_ok = TstNewPayment(order=order_ok)
    with pytest.raises(AlreadyPayedValidationError):
        payment_ok.get_payment_url()
    payment_ok.save_callbeck(order_ok_callback)
    assert payment_ok.order.paycallback.is_payed is True
    
def test_payment_error(order_error, order_error_callback):
    order_error = TstNewPayment(order=order_error)
    order_error.get_payment_url()
    order_error.save_callbeck(order_error_callback)
    with pytest.raises(ObjectDoesNotExist):
        order_error.order.paycallback.is_payed 

def test_order_not_checkout(order_not_checkout):
    with pytest.raises(NoCheckoutValidationError):
        TstNewPayment(order=order_not_checkout)

def test_payment_end_get_new_order(new_order, order_ok, order_ok_callback):
    payment_ok = TstNewPayment(order=order_ok)
    assert new_order().pk == payment_ok.order.pk
    payment_ok.save_callbeck(order_ok_callback)
    with pytest.raises(Http404):
        new_order()
