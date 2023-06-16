from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from app_order.models import Order
from app_order.serializers import OrderSerializer, OrderItemSerializer
from app_order.services import get_new_order_items, get_new_order


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_new_order_items(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderNewView(APIView):

    def get(self, request):
        serializer = OrderSerializer(get_new_order(request.user))
        return Response(serializer.data)
