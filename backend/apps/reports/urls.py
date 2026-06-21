# apps/reports/urls.py
from django.urls import path
from .views import CreateReportView, UpdateReportView, UserReportListView, AllReportsListView, LikeReportView

urlpatterns = [
    path('reports/', UserReportListView.as_view(), name='user-report-list'),
    path('reports/all/', AllReportsListView.as_view(), name='all-reports-list'),
    path('reports/create/', CreateReportView.as_view(), name='report-create'),
    path('reports/<int:pk>/edit/', UpdateReportView.as_view(), name='report-update'),
    path('reports/<int:pk>/like/', LikeReportView.as_view(), name='report-like'),
]
