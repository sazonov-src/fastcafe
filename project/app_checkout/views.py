from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from app_checkout.models import Checkout
from app_checkout.serializers import NewCheckoutSerializer, ManageCheckoutSerializer
from app_checkout.services import get_checkout, get_manage_checkout
from app_order.models import Order


class CheckoutAPI(APIView):
    serializer = NewCheckoutSerializer

    def get(self, request):
        try:
            serializer = self.serializer(get_checkout(request.user))
        except Order.DoesNotExist:
            return Response(
                {'not_found': 'Створіть спочатку замовлення'},
                status=status.HTTP_404_NOT_FOUND)
        except Checkout.DoesNotExist:
            return Response({})
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.validated_data)


class ManagerAPIView(APIView):
    serializer = ManageCheckoutSerializer

    def get(self, request, pk):
        serializer = self.serializer(get_manage_checkout(order_pk=pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = self.serializer(
            get_manage_checkout(order_pk=pk),
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)

