# apps/reports/urls.py
from django.urls import path
from .views import CreateReportView

urlpatterns = [
    path('reports/create/', CreateReportView.as_view(), name='report-create'),
]