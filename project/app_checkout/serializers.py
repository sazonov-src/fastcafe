from rest_framework.serializers import ModelSerializer

from app_checkout.models import Checkout


class CheckoutSerializerBase(ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'

