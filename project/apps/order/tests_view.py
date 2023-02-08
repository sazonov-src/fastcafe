from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from apps.menu.models import *
from apps.order.models import *
from apps.order.views import OrderViewSet


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
        request = self.factory.post(f'/api/v1/order/', data=request_data, format='json')
        response = self.view_post(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        request.user = self.user
        response = self.view_post(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create2(self):
        self.view_post = OrderViewSet.as_view({'post': 'create'})
        request_data = {'item': self.menu_item_child.pk, 'quantity': 0}
        request = self.factory.post(f'/api/v1/order/', data=request_data, format='json')
        request.user = self.user
        response = self.view_post(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        order_item, created = self.order.add_item(self.menu_item_child, 1)
        view_detail = OrderViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/api/v1/order/{order_item.pk}/')
        request.user = self.user
        response = view_detail(request, pk=123)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = view_detail(request, pk=order_item.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pk'], order_item.pk)

    def test_list(self):
        self.view_list = OrderViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/order/')
        request.user = self.user
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pk'], self.order.pk)

    def test_update(self):
        order_item, created = self.order.add_item(self.menu_item_child, 1)
        view_update = OrderViewSet.as_view({'put': 'update'})
        request = self.factory.put(f'/api/v1/order/{order_item.pk}/', {
            'quantity': 44
        }, format='json')
        request.user = self.user
        response = view_update(request, pk=123)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = view_update(request, pk=order_item.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 44)
        request = self.factory.put(f'/api/v1/order/{order_item.pk}/', {
            'quantity': 0}, format='json')
        request.user = self.user
        response = view_update(request, pk=order_item.pk)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_destroy(self):
        self.view_destroy = OrderViewSet.as_view({'delete': 'destroy'})
        order_item, created = self.order.add_item(self.menu_item_child, 1)
        request = self.factory.delete(f'/api/v1/order/{order_item.pk}/')
        request.user = self.user
        response = self.view_destroy(request, pk=123)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.view_destroy(request, pk=order_item.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
