from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from liqpay import LiqPay
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from app_order.models import Order
from app_order.services.new_order import NewOrder
from app_payment.models import PayCallback

from project import settings


class NoCheckoutValidationError(APIException):
    status_code = 400
    default_detail = "First, place your order"


class AlreadyPayedValidationError(APIException):
    status_code  = 400
    default_detail = "This order has already been paid"


class NewPayment:
    public_key = settings.LIQPAY_PUBLIC_KEY
    secret_key = settings.LIQPAY_SECRET_KEY
    liqpay = LiqPay(public_key, secret_key)
    server_url = settings.LIQPAY_DATA["server_url"].format(
        settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "localhost")

    def __init__(self, user):
        self._order = NewOrder(user=user)()
        if not self._order.is_checkout:
            raise NoCheckoutValidationError

    @property
    def order(self):
        return self._order

    @property
    def is_payment(self):
        return self.get_status_info()["status"] == "success"
     
    def get_payment_url(self):
        if self.is_payment:
            raise AlreadyPayedValidationError(_("This order has already been paid"))
        settings.LIQPAY_DATA.update({
            "amount": str(self._order.total_price),
            "order_id": str(self._order.pk),
            "server_url": self.server_url})
        return dict(url=self.liqpay.checkout_url(settings.LIQPAY_DATA))
    
    def get_status_info(self):
        return self.liqpay.api("request", {
            "action": "status",
            "order_id": self._order.pk })

    @classmethod
    def save_callbeck(cls, callbeck):
        sign = cls.liqpay.str_to_sign(cls.secret_key + callbeck["data"] + cls.secret_key)
        if sign != callbeck["signature"]:
            raise
        data = cls.liqpay.decode_data_from_str(callbeck["data"])
        if data["status"] != "success":
            return
        order = get_object_or_404(Order, pk=data["order_id"])
        PayCallback.objects.get_or_create(order=order, is_payed=True)
 

class OrderPayment(NewPayment):
    def __init__(self, order):
        self._order = self._get_order_with_int(order)

    @staticmethod
    def _get_order_with_int(order):
        if isinstance(order, Order):
            return order
        try:
            pk = int(order)
        except ValueError:
            raise ValidationError("This value can not be an identifier")
        return Order.objects.get(pk=pk)
