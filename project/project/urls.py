from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from app_checkout.views import NewCheckoutAPI
from app_menu.views import ItemChildViewSet, ItemViewSet, CategoryViewSet
from app_order.views import OrderItemViewSet, OrderNewView
from app_payment.views import GetPaymentUrlAPIView
from . import settings
from .view import auth_logout

router = routers.DefaultRouter()
router.register(r'item_child', ItemChildViewSet)
router.register(r'item', ItemViewSet)
router.register(r'category', CategoryViewSet)

new_order = routers.DefaultRouter()
new_order.register(r'items', OrderItemViewSet, basename='items')
# new_order.register(r'payment_responses', PaymentAPIResponseViewSet, basename='payment_responses')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/new_order/', OrderNewView.as_view()),
    path('api/v1/new_order/', include(new_order.urls)),
    path('api/v1/new_order/checkout/', NewCheckoutAPI.as_view()),
    path('api/v1/new_order/pay_url/', GetPaymentUrlAPIView.as_view()),
    # path('api/v1/new_order/pay_callback/', AcceptPaymentCallbackAPIView.as_view()),
    # path('api/v1/manager/orders/<int:pk>/checkout', ManagerCheckoutAPIView.as_view()),

    path(f'api/v1/auth_logout/', auth_logout),

    path('', include('social_django.urls', namespace='social')),
    # /login/github/ for github
    # /login/google-oauth2/ for google
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

