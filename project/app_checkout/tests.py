from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from app_checkout.services import get_new_checkout, create_new_checkout, get_manage_checkout
from app_menu.models import get_test_item
from app_order.services.new_order import update_or_create_new_order


class CheckoutTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.item = get_test_item()

    def test_update_or_create_checkout(self):
        with self.assertRaises(Http404):
            #  Помилка виникає тому шо Order не було створено
            create_new_checkout(
                user=self.user, user_name='Vasia', phone='+30987777777')
        update_or_create_new_order(user=self.user, item=self.item)
        checkout = create_new_checkout(
            user=self.user, user_name='Vasia')
        assert checkout.user_name == 'Vasia'
        assert checkout.order.created is True

    def test_get_checkout(self):
        with self.assertRaises(Http404):
            # виключиння виникфє тому що Order не створено
            get_new_checkout(self.user)
        (self.order, _), _ = update_or_create_new_order(user=self.user, item=self.item)
        with self.assertRaises(Http404):
            # виключиння виникфє тому що Checkout не створено
            get_new_checkout(self.user)
        checkout = create_new_checkout(
            user=self.user, user_name='Vasia', phone='+30987777777')
        assert checkout.user_name == 'Vasia'
        assert checkout.order.done is False
        with self.assertRaises(Http404):
            # так як замовлення вже оформлено воно стає created
            get_new_checkout(self.user)

    def test_get_manage_checkout(self):
        (self.order, _), _ = update_or_create_new_order(user=self.user, item=self.item)
        with self.assertRaises(Http404):
            get_manage_checkout(order_pk=self.order.pk)
        create_new_checkout(self.user, user_name="Vasia", phone='+30987777777')
        assert get_manage_checkout(order_pk=self.order.pk).pk == self.order.pk
