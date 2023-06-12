from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from app_menu.models import *
from app_menu.models import get_test_item
from app_order.models import Order, OrderItem, Checkout
from django.core.exceptions import ValidationError
from app_order.services import OrderService
from app_order.views import OrderViewSet


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = OrderService.objects.create(user=self.user)
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


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.menu_item_child = get_test_item()
        self.order = Order.objects.create(user=self.user)
        self.checkout = Checkout.objects.create(order=self.order)
        self.factory = APIRequestFactory()

    def test_create(self):
        self.view_post = OrderViewSet.as_view({'post': 'create'})
        request_data = {'item': self.menu_item_child.pk, 'quantity': 1}
        request = self.factory.post(f'/api/v1/app_order/', data=request_data, format='json')
        response = self.view_post(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.user
        response = self.view_post(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create2(self):
        self.view_post = OrderViewSet.as_view({'post': 'create'})
        request_data = {'item': self.menu_item_child.pk, 'quantity': 0}
        request = self.factory.post(f'/api/v1/app_order/', data=request_data, format='json')
        request.user = self.user
        response = self.view_post(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        order_item, created = self.order.add_item(self.menu_item_child, 1)
        view_detail = OrderViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/api/v1/app_order/{order_item.pk}/')
        request.user = self.user
        response = view_detail(request, pk=123)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = view_detail(request, pk=order_item.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pk'], order_item.pk)

    def test_list(self):
        self.view_list = OrderViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/app_order/')
        request.user = self.user
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pk'], self.order.pk)

    def test_update(self):
        order_item, created = self.order.add_item(self.menu_item_child, 1)
        view_update = OrderViewSet.as_view({'put': 'update'})
        request = self.factory.put(f'/api/v1/app_order/{order_item.pk}/', {
            'quantity': 44
        }, format='json')
        request.user = self.user
        response = view_update(request, pk=123)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = view_update(request, pk=order_item.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 44)
        request = self.factory.put(f'/api/v1/app_order/{order_item.pk}/', {
            'quantity': 0}, format='json')
        request.user = self.user
        response = view_update(request, pk=order_item.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy(self):
        self.view_destroy = OrderViewSet.as_view({'delete': 'destroy'})
        order_item, created = self.order.add_item(self.menu_item_child, 1)
        request = self.factory.delete(f'/api/v1/app_order/{order_item.pk}/')
        request.user = self.user
        response = self.view_destroy(request, pk=123)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.view_destroy(request, pk=order_item.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
