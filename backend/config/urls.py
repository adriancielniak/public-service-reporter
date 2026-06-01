"""
URL configuration for public-service-reporter project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def api_root(request):
    return JsonResponse({'message': 'Public Service Reporter API'})


def health(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),
    path('api/health/', health),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/v1/', include('rest_framework.urls')),
    path('api/', include('apps.service_auth.urls')),
    path('api/', include('apps.reports.urls')),
]
