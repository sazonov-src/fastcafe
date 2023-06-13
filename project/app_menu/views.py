from django.http import JsonResponse
from rest_framework.decorators import api_view, action
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app_menu.models import *
from app_menu import serializers


class ItemChildViewSet(ModelViewSet):
    queryset = MenuItemChild.objects.all()
    serializer_class = serializers.ItemChildSerializer


class ItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = serializers.ItemSerializer

    @action(methods=['get'], detail=True)
    def item_child(self, request, pk):
        title = self.queryset.get(pk=pk).title
        queryset = MenuItemChild.objects.filter(menu_item=pk)
        return Response({
            title: queryset.values()
        })


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
