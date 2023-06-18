from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from app_checkout.models import Checkout
from app_checkout.serializers import CheckoutSerializer
from app_checkout.services import get_checkout, update_or_create_checkout
from app_order.models import Order


class CheckoutAPI(APIView):

    def get(self, request):
        try:
            serializer = CheckoutSerializer(get_checkout(request.user))
        except Order.DoesNotExist:
            return Response(
                {'not_found': 'Створіть спочатку замовлення'}, status=status.HTTP_404_NOT_FOUND)
        except Checkout.DoesNotExist:
            return Response([])
        return Response(serializer.data)

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.validated_data)


