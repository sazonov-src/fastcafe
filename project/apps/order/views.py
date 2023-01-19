from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.order.models import Order
from apps.order.serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ViewSet):
    basename = 'order'
    # permission_classes = [IsAuthenticated]

    @property
    def order(self):
        return Order.objects.get_order(self.request.user)

    def list(self, request):
        serializer = OrderSerializer(self.order)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(self.order.order_items, pk=pk)
        serializer = OrderItemSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        request.data['user'] = self.order.user.pk
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)

    def update(self, request, pk=None):
        return self.create(request)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(self.order.order_items, pk=pk)
        instance.delete()
        return Response({'massage': 'Товар видалено'})
