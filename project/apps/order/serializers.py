from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.relations import PrimaryKeyRelatedField
from apps.menu.models import MenuItemChild
from apps.order.models import *


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
        fields = ('user', 'status', 'created_at', 'updated_at', 'order_items', 'total_price', 'item', 'quantity')
        extra_kwargs = {'status': {'required': False}}

    def save(self):
        user = self.validated_data['user']
        order = Order.objects.get(user=user)
        order.add_item(
            item=self.validated_data['item'],
            quantity=self.validated_data['quantity'])
        return order


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('order', 'user_name', 'phone', 'delivery', 'payment')
