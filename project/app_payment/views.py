from rest_framework import viewsets, views, response, status
from rest_framework.response import Response

from app_payment.serializers import GetPaymentUrlSerializer, PaymentCallbackSerializer
from app_payment.services import get_payment_url, manage_payment_callback, get_payment_callback_queryset


class GetPaymentUrlAPIView(views.APIView):

    def get(self, request):
        url = get_payment_url(request.user)
        serializer = GetPaymentUrlSerializer({"url": url})
        return Response(serializer.data)


class AcceptPaymentCallbackAPIView(views.APIView):

    def get(self, request):
        serializer = PaymentCallbackSerializer(
            get_payment_callback_queryset(user=request.user), many=True)
        return Response(serializer.data)

    def post(self, request):
        callback = manage_payment_callback(request.data)
        serializer = PaymentCallbackSerializer(data=callback)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_201_CREATED)
