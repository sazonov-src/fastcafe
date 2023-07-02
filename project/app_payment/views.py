from rest_framework import views, status
from rest_framework.response import Response

from app_payment.models import PaymentCallback
from app_payment.serializers import PaymentCallbackSerializer
from app_payment.services import get_payment_url, manage_payment_callback, get_payment_callback_queryset


class GetPaymentUrlAPIView(views.APIView):

    def get(self, request):
        return Response(get_payment_url(request.user))


class AcceptPaymentCallbackAPIView(views.APIView):

    def get(self, request):
        serializer = PaymentCallbackSerializer(
            get_payment_callback_queryset(user=request.user), many=True)
        return Response(serializer.data)

    def post(self, request):
        callback_data = manage_payment_callback(request.data)
        obj = PaymentCallback.objects.get(pk=callback_data.pop("pk"))
        serializer = PaymentCallbackSerializer(obj, data=callback_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_201_CREATED)
