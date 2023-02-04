from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(http_method_names=['POST'])
def auth_logout(request):
    logout(request)
    return Response({'acces': 'good'})
