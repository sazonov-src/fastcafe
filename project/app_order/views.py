from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from app_order.models import Order
from app_order.serializers import OrderSerializer, OrderItemSerializer
from app_order.services import get_new_order_items, get_new_order, delete_order_item


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_new_order_items(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_order_item(order_item=instance)


class OrderNewView(APIView):

    def get(self, request):
        try:
            serializer = OrderSerializer(get_new_order(request.user))
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'Додайте хочаб одну позицію в замовлення'},
                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)
