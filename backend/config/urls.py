"""
URL configuration for public-service-reporter project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({'message': 'Public Service Reporter API'})


def health(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/health/', health),
    path('api/v1/', include('rest_framework.urls')),
]
