from django.urls import path
from .views import CreateTicketView, AssignTicketView

urlpatterns = [
    path('tickets/create/', CreateTicketView.as_view(), name='ticket-create'),
path('tickets/<int:pk>/assign/', AssignTicketView.as_view(), name='ticket-assign'),
]