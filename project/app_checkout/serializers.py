from rest_framework.serializers import ModelSerializer

from app_checkout.models import Checkout
from app_checkout.services import update_or_create_checkout


class CheckoutSerializer(ModelSerializer):
    class Meta:
        model = Checkout
        fields = '__all__'
        read_only_fields = ['order', 'is_paid', 'done']

    def save(self, **kwargs):
        update_or_create_checkout(user=kwargs['user'], **self.validated_data)

