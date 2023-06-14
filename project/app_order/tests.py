from django.contrib.auth.models import User
from django.test import TestCase

from app_menu.models import get_test_item
from .models import Order, OrderItem, Checkout

from .services import update_or_create_order


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword')
        self.item = get_test_item()
        self.item2 = get_test_item(2)

    def test_update_or_create_order(self):
        assert len(Order.objects.all()) == 0  # жодного замовлення
        (order, is_created_order), (item, _) = update_or_create_order(user=self.user, item=self.item)
        # створюєм нове замовлення
        assert is_created_order is True  # замовлення створене
        assert len(order.orderitem_set.all()) == 1  # в замовленні одна позиція
        assert len(Order.objects.all()) == 1
        assert item.quantity == 1
        order.status = 'created'
        order.save()
        (order, is_created_order), (item, _) = update_or_create_order(user=self.user, item=self.item2, quantity=2)
        assert is_created_order is True
        assert len(Order.objects.all()) == 2
        assert len(order.orderitem_set.all()) == 1
        assert item.quantity == 2
        (order, is_created_order), _ = update_or_create_order(user=self.user2, item=self.item2)
        assert len(Order.objects.all()) == 3
        assert len(order.orderitem_set.all()) == 1
        (order, is_created_order), (item, _) = update_or_create_order(user=self.user, item=self.item)
        # створюєм нове замовлення
        assert is_created_order is False  # замовлення взяте

    def test_total_price(self):
        (order, _), _ = update_or_create_order(user=self.user, item=self.item)
        assert order.total_price == 25
        (order, _), _ = update_or_create_order(user=self.user, item=self.item2, quantity=2)
        assert order.total_price == 75
