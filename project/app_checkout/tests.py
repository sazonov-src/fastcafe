from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from app_checkout.models import Checkout
from app_checkout.services import get_checkout, update_or_create_checkout
from app_menu.models import get_test_item, Category
from app_order.models import Order
from app_order.services import update_or_create_order


class CheckoutTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.item = get_test_item()

    def test_update_or_create_checkout(self):
        with self.assertRaises(Order.DoesNotExist):
            #  Помилка виникає тому шо Order не було створено
            update_or_create_checkout(
                user=self.user, user_name='Vasia', payment='card', phone='+30987777777')
        update_or_create_order(user=self.user, item=self.item)
        checkout, is_created = update_or_create_checkout(
            user=self.user, user_name='Vasia', payment='card')
        assert (checkout.user_name, is_created) == ('Vasia', True)

    def test_get_checkout(self):
        with self.assertRaises(Order.DoesNotExist):
            # виключиння виникфє тому що Order не створено
            get_checkout(self.user)
        (self.order, _), _ = update_or_create_order(user=self.user, item=self.item)
        with self.assertRaises(Checkout.DoesNotExist):
            # виключиння виникфє тому що Checkout не створено
            get_checkout(self.user)
        update_or_create_checkout(
            user=self.user, user_name='Vasia', payment='card', phone='+30987777777', done=False)
        assert get_checkout(self.user).user_name == 'Vasia'
        assert get_checkout(self.user).done is False
