from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apps.menu.views import ItemChildViewSet, ItemViewSet, CategoryViewSet
from apps.order.views import OrderViewSet
from project import settings
from project.view import auth_logout


router = routers.DefaultRouter()

router.register(r'item_child', ItemChildViewSet)
router.register(r'item', ItemViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'order', OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/manager', include(router.urls)),

    path(f'auth_logout/', auth_logout),

    path('', include('social_django.urls', namespace='social')),
    # http://127.0.0.1:8000/login/github/ for github
    # http://127.0.0.1:8000/login/google-oauth2/ for google


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
