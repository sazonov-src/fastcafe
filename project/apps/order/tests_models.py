from django.contrib.auth.models import User
from django.test import TestCase
from apps.menu.models import *
from apps.order.models import Order, OrderItem
from django.core.exceptions import ValidationError

class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(user=self.user)
        self.item = get_test_item()

    def test_str_representation(self):
        # Перевірка чи вірно відображається рядок замовлення
        self.assertEqual(str(self.order), 'testuser - new')

    def test_total_price(self):
        # Додати елемент до замовлення та перевірити чи вірна сума
        self.order.add_item(self.item, 2)
        self.assertEqual(self.order.total_price, self.item.price * 2)

    def test_add_item(self):
        # Додати елемент до створеного замовлення
        self.order.add_item(self.item, 2)
        self.assertEqual(self.order.orderitem_set.get(item=self.item).quantity, 2)
        self.order.add_item(self.item, 5)
        self.assertEqual(self.order.orderitem_set.get(item=self.item).quantity, 5)

    def test_new_status(self):
        # При створенні нового замовленя статус має бути завжди new
        created_order = Order.objects.create(user=self.user, status='created')
        self.assertEqual(created_order.status, 'new')

    def test_status_change(self):
        # При створенні нового замовленя статус має бути завжди new
        created_order = Order.objects.create(user=self.user, status='new')
        created_order.status = 'created'
        created_order.save()
        self.assertEqual(created_order.status, 'created')


class OrderItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.order = Order.objects.create(user=self.user)
        category = Category.objects.create(title='категорія')
        menu_item = MenuItem.objects.create(title='тестовий item',
                                            category=category,
                                            description='опис')
        self.item = MenuItemChild.objects.create(subtitle='Test Item',
                                                 menu_item=menu_item,
                                                 price=25)

    def test_plus_quantity(self):
        order_item = OrderItem.objects.create(order=self.order, item=self.item, quantity=1)
        order_item.plus_quantity()
        self.assertEqual(order_item.quantity, 2)

    def test_minus_quantity(self):
        order_item = OrderItem.objects.create(order=self.order, item=self.item, quantity=2)
        order_item.minus_quantity()
        self.assertEqual(order_item.quantity, 1)
        with self.assertRaises(ValueError):
            order_item.minus_quantity()
        self.assertEqual(order_item.quantity, 1)

