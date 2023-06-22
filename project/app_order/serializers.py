from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from app_order.models import *
from app_order.services.manager import mark_order_as_done
from app_order.services.new_order import update_or_create_new_order


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('pk', 'item', 'quantity', 'total_price')

    def save(self, **kwargs):
        update_or_create_new_order(
            user=kwargs['user'],
            item=self.validated_data['item'],
            quantity=self.validated_data['quantity'])


class OrderSerializer(serializers.ModelSerializer):
    checkout = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class ManagerOrderSerializer(serializers.ModelSerializer):
    checkout = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('created', 'user')

    def update(self, instance, validated_data):
        mark_order_as_done(
            instance=instance,
            data=validated_data)
        return instance


class ManagerOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'
