from rest_framework.views import APIView
from rest_framework.response import Response

from app_checkout.serializers import NewCheckoutSerializer, ManageCheckoutSerializer
from app_checkout.services import get_new_checkout, get_manage_checkout


class NewCheckoutAPI(APIView):
    serializer = NewCheckoutSerializer

    def get(self, request):
        serializer = self.serializer(
            get_new_checkout(request.user))
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.validated_data)


class ManagerCheckoutAPIView(APIView):
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

