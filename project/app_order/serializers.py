from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from app_menu.models import MenuItemChild
from app_order.models import *
from app_order.services import OrderService


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('pk', 'item', 'quantity', 'total_price')


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)
    item = PrimaryKeyRelatedField(queryset=MenuItemChild.objects.all(), write_only=True)
    quantity = IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'user', 'status', 'created_at', 'updated_at', 'order_items', 'total_price', 'item', 'quantity')
        extra_kwargs = {'status': {'required': False}}

    def create(self, validated_data):
        user = validated_data['user']
        order = Order.objects.get(user=user)
        order.add_item(
            item=validated_data['item'],
            quantity=validated_data['quantity'])
        return order

    def update(self, instance, validated_data):
        instance.quantity = validated_data['quantity']
        instance.save()
        return instance


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('app_order', 'user_name', 'phone', 'delivery', 'payment')
