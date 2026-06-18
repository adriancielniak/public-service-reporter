from django.urls import path
from .views import CreateTicketView

urlpatterns = [
    path('tickets/create/', CreateTicketView.as_view(), name='ticket-create'),
]