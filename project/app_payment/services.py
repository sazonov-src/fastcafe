from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from liqpay import LiqPay
from app_order.models import Order

from project import settings


class NoCheckoutValidationError(ValidationError):
    pass


class AlreadyPayedValidationError(ValidationError):
    pass


class NewPayment:
    public_key = settings.LIQPAY_PUBLIC_KEY
    secret_key = settings.LIQPAY_SECRET_KEY
    liqpay = LiqPay(public_key, secret_key)


    def __init__(self, order):
        self._order = self._get_order_with_int(order)
        if not self._order.is_checkout:
            raise NoCheckoutValidationError(_("First, place your order"))


    def _get_order_with_int(self, order):
        if isinstance(order, Order):
            return order
        try:
            pk = int(order)
        except ValueError:
            raise ValidationError("This value can not be an identifier")
        return Order.objects.get(pk=pk)
     

    def is_payment(self):
        return self.get_status_info()["result"] == "ok"

     
    def get_payment_url(self):
        if self.is_payment():
            raise AlreadyPayedValidationError(_("This order has already been paid"))
        settings.LIQPAY_DATA.update({
            "amount": str(self._order.total_price),
            "order_id": str(self._order.pk)})
        return dict(url=self.liqpay.checkout_url(settings.LIQPAY_DATA))

    
    def get_status_info(self):
        return self.liqpay.api("request", {
            "action": "status",
            "order_id": self._order.pk })
