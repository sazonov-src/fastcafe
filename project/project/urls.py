from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from project import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/menu/', include('apps.menu.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
