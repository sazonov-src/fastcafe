from django.urls import path, include
from rest_framework import routers
from apps.menu.views import *


router = routers.SimpleRouter()
router.register(r'item_child', ItemChildViewSet)
router.register(r'item', ItemViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
