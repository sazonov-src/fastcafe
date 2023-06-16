from rest_framework import serializers
from rest_framework.fields import IntegerField, DecimalField
from rest_framework.relations import PrimaryKeyRelatedField
from app_menu.models import MenuItemChild
from app_order.models import *
from app_order.services import update_or_create_order


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('pk', 'item', 'quantity', 'total_price')

    def save(self, **kwargs):
        update_or_create_order(
            user=kwargs['user'],
            item=self.validated_data['item'],
            quantity=self.validated_data['quantity'])


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'
