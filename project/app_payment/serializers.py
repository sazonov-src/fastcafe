from rest_framework import serializers

from app_payment.models import PaymentCallback


class GetPaymentUrlSerializer(serializers.Serializer):
    url = serializers.CharField()


class PaymentCallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCallback
        fields = "__all__"
