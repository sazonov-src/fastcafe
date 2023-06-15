from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app_order.models import Order
from app_order.serializers import OrderSerializer, OrderItemSerializer, CheckoutSerializer


class OrderViewSet(viewsets.ViewSet):
    basename = 'app_order'
    permission_classes = [IsAuthenticated]

    @property
    def order(self):
        return Order.objects.get_or_create(user=self.request.user)[0]

    def list(self, request):
        serializer = OrderSerializer(self.order)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order_item = get_object_or_404(self.order.orderitem_set.all(), pk=pk)
        serializer = OrderItemSerializer(order_item)
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
        order_item = get_object_or_404(self.order.orderitem_set.all(), pk=pk)
        order_item.delete()
        return Response({'massage': 'Товар видалено'})

    @action(detail=False, methods=['get', 'post', 'put'])
    def checkout(self, request):
        if request.method == 'POST':
            serializer = CheckoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(request.data)
        else:
            try:
                checkout = self.order.checkout
            except Order.checkout.RelatedObjectDoesNotExist:
                return Response(
                    {'massage': 'Замовлення не оформлене'},
                    status=status.HTTP_204_NO_CONTENT)
        if request.method == 'PUT':
            serializer = CheckoutSerializer(checkout, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(request.data)
        if request.method == 'GET':
            serializer = CheckoutSerializer(checkout)
            return Response(serializer.data)


class OrderManagerViewSet(viewsets.ModelViewSet):
    pass
