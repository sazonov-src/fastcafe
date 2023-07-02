from rest_framework import serializers

from app_payment.models import PaymentCallback


class PaymentCallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCallback
        fields = ("action", "status", "data")
