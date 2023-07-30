from rest_framework.views import APIView
from rest_framework.response import Response

from app_checkout.serializers import NewCheckoutSerializer
from app_checkout.services import NewCheckout


class NewCheckoutAPI(APIView):
    serializer = NewCheckoutSerializer

    @property
    def new_checkout(self):
        return NewCheckout(self.request.user)

    def get(self, request):
        serializer = self.serializer(self.new_checkout())
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer(
            data=self.new_checkout.get_create_or_update_data(**request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

