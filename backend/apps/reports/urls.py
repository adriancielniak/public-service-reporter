# apps/reports/urls.py
from django.urls import path
from .views import CreateReportView, UpdateReportView

urlpatterns = [
    path('reports/create/', CreateReportView.as_view(), name='report-create'),
    # <int:pk> to id raportu
    path('reports/<int:pk>/edit/', UpdateReportView.as_view(), name='report-update'),
]