# apps/reports/views.py
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Report, AdminComment, StatusChange, UserComment
from .serializers import ReportSerializer, AdminReportSerializer, AdminCommentSerializer, UserCommentSerializer
from apps.service_auth.permissions import IsOwner, IsAdmin


# POST /api/reports/create/
class CreateReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReportSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PATCH /api/reports/<int:pk>/edit/
class UpdateReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        self.check_object_permissions(request, report)
        serializer = ReportSerializer(report, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET /api/reports/
class UserReportListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reports = Report.objects.filter(user=request.user).order_by('-created_at')
        serializer = ReportSerializer(reports, many=True, context={'request': request})
        return Response(serializer.data)


# GET /api/reports/all/
class AllReportsListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True, context={'request': request})
        return Response(serializer.data)


# POST /api/reports/<int:pk>/like/
class LikeReportView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)

        if report.user == request.user:
            return Response(
                {'detail': 'Nie możesz potwierdzić własnego zgłoszenia.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if report.liked_by.filter(pk=request.user.pk).exists():
            report.liked_by.remove(request.user)
            Report.objects.filter(pk=pk).update(likes=F('likes') - 1)
        else:
            report.liked_by.add(request.user)
            Report.objects.filter(pk=pk).update(likes=F('likes') + 1)

        report.refresh_from_db()
        serializer = ReportSerializer(report, context={'request': request})
        return Response(serializer.data)


# GET /api/reports/<int:pk>/
class ReportDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        serializer = ReportSerializer(report, context={'request': request})
        return Response(serializer.data)


# GET+POST /api/reports/<int:pk>/comments/
class UserCommentListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        comments = report.user_comments.all()
        serializer = UserCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        text = request.data.get('text', '').strip()
        if not text:
            return Response({'detail': 'Komentarz nie może być pusty.'}, status=status.HTTP_400_BAD_REQUEST)
        comment = UserComment.objects.create(report=report, author=request.user, text=text)
        return Response(UserCommentSerializer(comment, context={'request': request}).data, status=status.HTTP_201_CREATED)


# DELETE /api/reports/<int:pk>/comments/<int:comment_pk>/
class UserCommentDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, comment_pk):
        comment = get_object_or_404(UserComment, pk=comment_pk, report_id=pk)
        if comment.author != request.user:
            return Response({'detail': 'Nie możesz usunąć cudzego komentarza.'}, status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Admin views ────────────────────────────────────────────────────────────────

# GET /api/admin/reports/
class AdminReportListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        status_filter = request.query_params.get('status')
        reports = Report.objects.all()
        if status_filter:
            reports = reports.filter(status=status_filter)
        serializer = AdminReportSerializer(reports, many=True)
        return Response(serializer.data)


# PATCH /api/admin/reports/<int:pk>/status/
class AdminUpdateStatusView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        new_status = request.data.get('status')

        valid = [s[0] for s in Report.STATUS_CHOICES]
        if new_status not in valid:
            return Response({'detail': 'Nieprawidłowy status.'}, status=status.HTTP_400_BAD_REQUEST)

        if report.status != new_status:
            StatusChange.objects.create(
                report=report,
                changed_by=request.user,
                old_status=report.status,
                new_status=new_status,
            )
            report.status = new_status
            report.save()

        serializer = AdminReportSerializer(report)
        return Response(serializer.data)


# POST /api/admin/reports/<int:pk>/comments/
class AdminCommentCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        text = request.data.get('text', '').strip()
        if not text:
            return Response({'detail': 'Komentarz nie może być pusty.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = AdminComment.objects.create(report=report, author=request.user, text=text)
        return Response(AdminCommentSerializer(comment).data, status=status.HTTP_201_CREATED)
