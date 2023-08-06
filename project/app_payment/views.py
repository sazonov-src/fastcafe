from rest_framework import views, status
from rest_framework.response import Response

from app_payment.services import NewPayment


class GetPaymentUrlAPIView(views.APIView):

    def get(self, request):
        return Response(NewPayment(request.user).get_payment_url())


class PayCallbackAPIView(views.APIView):

    def post(self, request):
        NewPayment.save_callbeck(callbeck=request.data)
        return Response({"status":"success"})
