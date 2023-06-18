from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from app_checkout.views import CheckoutAPI
from app_menu.views import ItemChildViewSet, ItemViewSet, CategoryViewSet
from app_order.views import OrderItemViewSet, OrderNewView
from . import settings
from .view import auth_logout

router = routers.DefaultRouter()
router.register(r'item_child', ItemChildViewSet)
router.register(r'item', ItemViewSet)
router.register(r'category', CategoryViewSet)


new_order = routers.DefaultRouter()
new_order.register(r'', OrderItemViewSet, basename='new_order_items')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/manager/', include(router.urls)),
    path('api/v1/new_order/', OrderNewView.as_view()),
    path('api/v1/new_order/items/', include(new_order.urls)),
    path('api/v1/new_order/checkout/', CheckoutAPI.as_view()),

    path(f'api/v1/auth_logout/', auth_logout),

    path('', include('social_django.urls', namespace='social')),
    # http://127.0.0.1:8000/login/github/ for github
    # http://127.0.0.1:8000/login/google-oauth2/ for google


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
