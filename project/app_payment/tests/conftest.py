import pytest
from app_order.services.new_order import NewOrder

from app_payment.services import NewPayment, NoCheckoutValidationError

pytestmark = [pytest.mark.django_db]


class TstNewPayment(NewPayment):
    server_url = "https://7ba7-109-108-232-220.ngrok-free.app"
    def __init__(self, order):
        self._order = order
        if not self._order.is_checkout:
            raise NoCheckoutValidationError


def order_creator(mixer, menu_item, user, pk):
    order = mixer.blend("app_order.order", pk=pk, user=user)
    mixer.blend("app_order.orderitem", order=order, item=menu_item, quantity=1)
    return order

def order_checkout(checkout_default):
    checkout_default.order

def get_callback_data(file_name, signature):
    with open(f"app_payment/tests/{file_name}.txt", "r") as file:
        f = file.read().strip()
    return {
        "data": f,
        "signature": signature}
    

@pytest.fixture
def pk_ok():
    return 454545

@pytest.fixture
def pk_error():
    return 10001

@pytest.fixture
def order_ok(mixer, menu_item, user, pk_ok, checkout_default):
    order_creator(mixer, menu_item, user, pk_ok)
    return checkout_default().order

@pytest.fixture
def order_ok_callback():
    return get_callback_data("data_ok", "cGMTjuxp4lJNUdpzdT1VhY6ugI8=")

@pytest.fixture
def order_error(mixer, menu_item, user, pk_error, checkout_default):
    order_creator(mixer, menu_item, user, pk_error)
    return checkout_default().order

@pytest.fixture
def order_error_callback():
    return get_callback_data("data_error", "IP0+dp5Md1G6cHogNscsnWWihHM=")
    
@pytest.fixture
def order_not_checkout(mixer, menu_item, user, pk_ok):
    return order_creator(mixer, menu_item, user, pk_ok)

@pytest.fixture
def new_order(user):
    return NewOrder(user=user)



