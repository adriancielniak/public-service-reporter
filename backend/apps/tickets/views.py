# apps/tickets/views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Ticket
from .serializers import TicketSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# POST /api/tickets/create/
class CreateTicketView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# PATCH /api/tickets/<int:pk>/assign/
class AssignTicketView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)

        worker_id = request.data.get('assigned_to')

        if worker_id:
            worker = get_object_or_404(User, id=worker_id)
        else:
            worker = request.user

        old_worker = ticket.assigned_to
        ticket.assigned_to = worker

        if ticket.status == 'new':
            ticket.status = 'assigned'
            ticket.updates.append(f"Ticket status changed to 'assigned'. Assigned to {worker.username}.")
        else:
            if old_worker and old_worker != worker:
                ticket.updates.append(f"Worker changed from {old_worker.username} to {worker.username}.")
            elif not old_worker:
                ticket.updates.append(f"Assigned to {worker.username}.")

        ticket.save()

        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)