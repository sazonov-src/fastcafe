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
        self._order = Order.objects.get(pk=order) if isinstance(order, str) else order        
        if not self._order.is_checkout:
            raise NoCheckoutValidationError(_("First, place your order"))
     

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


#
# def _validate_callback_data(data):
#     try:
#         sign = liqpay.str_to_sign(settings.LIQPAY_SECRET_KEY + data['data'] + settings.LIQPAY_SECRET_KEY)
#         if sign != data['signature']:
#             raise ValidationError(_('This data is not valid'))
#     except KeyError:
#         raise ValidationError
#
#
# def _validate_order_callbacks(order: Order):
#     try:
#         order.paymentcallback_set.get(status='success')
#         raise ValidationError(_("The order is successfully placed"))
#     except ObjectDoesNotExist:
#         return order
#
#
# def get_payment_url(user: User):
#     order = get_new_order(user=user)
#     order = _validate_order_callbacks(order=order)
#     callback, _ = PaymentCallback.objects.get_or_create(order=order, data="")
#     host = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "localhost"
#     settings.LIQPAY_DATA['result_url'].format(host)
#     settings.LIQPAY_DATA['server_url'].format(host)
#     settings.LIQPAY_DATA.update({
#         "amount": str(order.total_price),
#         "order_id": str(callback.pk)})
#     return dict(url=liqpay.checkout_url(settings.LIQPAY_DATA))
#
#
# def manage_payment_callback(data: dict) -> dict:
#     _validate_callback_data(data)
#     res = liqpay.decode_data_from_str(data['data'])
#     try:
#         PaymentCallback.objects.get(data=data['data'])
#         raise ValidationError(_('This data has already been saved'))
#     except ObjectDoesNotExist:
#         return {"pk": res['order_id'],
#                 "action": res['action'],
#                 "status": res['status'],
#                 "data": data['data']}
#
#
# def get_payment_callback_queryset(user: User):
#     order = get_new_order(user=user)
#     return order.paymentcallback_set.all()
#
#
