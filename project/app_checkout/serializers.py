from rest_framework.serializers import ModelSerializer

from app_checkout.models import Checkout
from app_checkout.services import create_new_checkout


class CheckoutSerializerBase(ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'
        read_only_fields = ['order', 'is_paid']


class NewCheckoutSerializer(CheckoutSerializerBase):

    def save(self, **kwargs):
        create_new_checkout(user=kwargs['user'], **self.validated_data)


class ManageCheckoutSerializer(CheckoutSerializerBase):
    pass

