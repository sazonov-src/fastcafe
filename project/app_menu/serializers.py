from rest_framework import serializers
from app_menu.models import *


class ItemChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemGeneral
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
