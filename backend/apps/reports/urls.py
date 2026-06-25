# apps/reports/urls.py
from django.urls import path
from .views import (
    CreateReportView, UpdateReportView, UserReportListView,
    AllReportsListView, LikeReportView, ReportDetailView,
    UserCommentListCreateView, UserCommentDeleteView,
    AdminReportListView, AdminUpdateStatusView, AdminCommentCreateView,
)

urlpatterns = [
    # Użytkownik
    path('reports/', UserReportListView.as_view(), name='user-report-list'),
    path('reports/all/', AllReportsListView.as_view(), name='all-reports-list'),
    path('reports/create/', CreateReportView.as_view(), name='report-create'),
    path('reports/<int:pk>/edit/', UpdateReportView.as_view(), name='report-update'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('reports/<int:pk>/like/', LikeReportView.as_view(), name='report-like'),
    path('reports/<int:pk>/comments/', UserCommentListCreateView.as_view(), name='report-comments'),
    path('reports/<int:pk>/comments/<int:comment_pk>/', UserCommentDeleteView.as_view(), name='report-comment-delete'),

    # Admin
    path('admin/reports/', AdminReportListView.as_view(), name='admin-report-list'),
    path('admin/reports/<int:pk>/status/', AdminUpdateStatusView.as_view(), name='admin-report-status'),
    path('admin/reports/<int:pk>/comments/', AdminCommentCreateView.as_view(), name='admin-report-comment'),
]
