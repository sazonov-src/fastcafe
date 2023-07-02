from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _
from liqpay import LiqPay
from rest_framework.exceptions import ValidationError


from app_order.services.new_order import get_new_order
from app_payment.models import PaymentCallback
from project import settings

liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_SECRET_KEY)


def _validate_callback_data(data):
    try:
        sign = liqpay.str_to_sign(settings.LIQPAY_SECRET_KEY + data['data'] + settings.LIQPAY_SECRET_KEY)
        if sign != data['signature']:
            raise ValidationError(_('This data is not valid'))
    except KeyError:
        raise ValidationError


def get_payment_url(user: User):
    order = get_new_order(user=user)
    settings.LIQPAY_DATA.update({
        "amount": str(order.total_price),
        "order_id": str(order.pk)})
    return liqpay.checkout_url(settings.LIQPAY_DATA)


def manage_payment_callback(data: dict) -> dict:
    _validate_callback_data(data)
    res = liqpay.decode_data_from_str(data['data'])
    try:
        PaymentCallback.objects.get(data=data['data'])
        raise ValidationError(_('This data has already been saved'))
    except ObjectDoesNotExist:
        return {"order": res['order_id'],
                "action": res['action'],
                "status": res['status'],
                "data": data['data']}


def get_payment_callback_queryset(user: User):
    order = get_new_order(user=user)
    return order.paymentcallback_set.all()


