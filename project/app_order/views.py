from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.formatting import re

from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from app_order.serializers import NewOrderSerializer, NewOrderItemSerializer 
from app_order.services.manager import *
from app_order.services.new_order import *


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = NewOrderItemSerializer
    permission_classes = [IsAuthenticated]

    @property
    def order(self):
        return NewOrder(user=self.request.user)

    def get_queryset(self):
        return self.order.orderitems_queryset

    def perform_create(self, serializer):
        serializer.save(self.order)

    def perform_destroy(self, instance):
        self.order.delete(item=instance)


class OrderNewView(APIView):
    serializer_class = NewOrderSerializer
    permission_classes = [IsAuthenticated]
    
    @property
    def order(self):
        return NewOrder(user=self.request.user)

    def get(self, request):
        serializer = self.serializer_class(self.order())
        return Response(serializer.data)
