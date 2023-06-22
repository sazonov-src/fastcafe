from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from app_order.serializers import NewOrderSerializer, NewOrderItemSerializer, ManagerOrderSerializer, \
    ManagerOrderItemSerializer
from app_order.services.manager import *
from app_order.services.new_order import *


class ManageOrderViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    serializer_class = ManagerOrderSerializer

    def get_queryset(self):
        return get_in_process_orders_queryset()

    @action(detail=True)
    def items(self, request, pk=None):
        serializer = ManagerOrderItemSerializer(
            get_order_items_queryset(order_pk=pk), many=True,)
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = NewOrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_new_orderitems_queryset(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_new_order_item(order_item=instance)


class OrderNewView(APIView):
    serializer_class = NewOrderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.serializer_class(get_new_order(request.user))
        return Response(serializer.data)
