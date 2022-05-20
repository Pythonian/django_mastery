"""config project URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('django.contrib.auth.urls')),
    path('', include('human_resource.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'human_resource.views.error_500'
handler404 = 'human_resource.views.error_404'
