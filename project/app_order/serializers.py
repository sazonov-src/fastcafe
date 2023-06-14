from rest_framework import serializers
from rest_framework.fields import IntegerField, DecimalField
from rest_framework.relations import PrimaryKeyRelatedField
from app_menu.models import MenuItemChild
from app_order.models import *
from app_order.services import update_or_create_order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('pk', 'item', 'quantity', 'total_price')


class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, required=False)
    item = PrimaryKeyRelatedField(queryset=MenuItemChild.objects.all(), write_only=True)
    quantity = IntegerField(min_value=1, write_only=True)

    class Meta:
        model = Order
        fields = (
            'pk', 'user', 'status', 'created_at', 'updated_at', 'orderitem_set', 'total_price', 'item', 'quantity'
        )
        extra_kwargs = {'status': {'required': False}}

    def save(self, **kwargs):
        update_or_create_order(
            user=self.validated_data['user'],
            item=self.validated_data['item'],
            quantity=self.validated_data['quantity'])


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkout
        fields = ('app_order', 'user_name', 'phone', 'delivery', 'payment')
