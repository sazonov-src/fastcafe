from django.contrib.auth.models import User
from django.test import TestCase
from liqpay import LiqPay
from rest_framework.exceptions import ValidationError
from rest_framework.templatetags import rest_framework

from app_menu.models import get_test_item
from app_order.services.new_order import update_or_create_new_order
from app_payment.models import PaymentCallback
from app_payment.services import get_payment_url, manage_payment_callback
from project import settings


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.item = get_test_item()
        (self.order, _), _ = update_or_create_new_order(user=self.user, item=self.item)

    def test_get_payment_url(self):
        assert get_payment_url(user=self.user) == get_payment_url(user=self.user)

    def test_manage_payment_callback(self):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_SECRET_KEY)
        d = {'language': 'uk', 'currency': 'UAH', 'amount': 1.0, 'payment_id': 2333180919, 'action': 'pay', 'status': 'success', 'version': 3, 'type': 'buy', 'paytype': 'gpaycard', 'public_key': 'sandbox_i63394948889', 'acq_id': 414963, 'order_id': '1', 'liqpay_order_id': 'KKC3UGL01688062960452782', 'description': 'description\ntext', 'sender_phone': '380985827925'}
        callback = {
            'data': liqpay.cnb_data(d),
            'signature': liqpay.cnb_signature(d)}
        payment_callback = manage_payment_callback(data=callback)
        assert payment_callback["data"] == callback["data"]
        callback.update({'signature': "fail_signature"})
        with self.assertRaises(ValidationError):
            manage_payment_callback(data=callback)
        payment_callback.update(dict(order=self.order))
        obj = PaymentCallback.objects.create(**payment_callback)
        assert obj.order == self.order
