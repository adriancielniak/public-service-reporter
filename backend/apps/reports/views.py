# apps/reports/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import ReportSerializer


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