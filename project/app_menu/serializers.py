from rest_framework import serializers
from apps.menu.models import *


class ItemChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemChild
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
