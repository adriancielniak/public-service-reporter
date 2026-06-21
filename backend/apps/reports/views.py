# apps/reports/views.py
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Report
from .serializers import ReportSerializer
from apps.service_auth.permissions import IsOwner

# POST /api/reports/create/
class CreateReportView(APIView):
    authentication_classes = [TokenAuthentication]
    # user musi byc zalogowany
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # request w kontekście, aby serializer miał dostęp do request.user
        serializer = ReportSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PATCH /api/reports/<int:pk>/edit/
class UpdateReportView(APIView):
    authentication_classes = [TokenAuthentication]
    # zalogowany i wlasciciel raportu
    permission_classes = [IsAuthenticated, IsOwner]

    def patch(self, request, pk):
        # pobierz raport (lub 404)
        report = get_object_or_404(Report, pk=pk)


        self.check_object_permissions(request, report)

        # partial=True bo tylko edycja
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
        # order by najnowsze
        reports = Report.objects.filter(user=request.user).order_by('-created_at')

        # many=True bo lista
        serializer = ReportSerializer(reports, many=True)

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
            return Response({'detail': 'Nie możesz potwierdzić własnego zgłoszenia.'}, status=status.HTTP_403_FORBIDDEN)

        if report.liked_by.filter(pk=request.user.pk).exists():
            report.liked_by.remove(request.user)
            Report.objects.filter(pk=pk).update(likes=F('likes') - 1)
        else:
            report.liked_by.add(request.user)
            Report.objects.filter(pk=pk).update(likes=F('likes') + 1)

        report.refresh_from_db()
        serializer = ReportSerializer(report, context={'request': request})
        return Response(serializer.data)
