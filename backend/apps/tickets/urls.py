from django.urls import path
from .views import CreateTicketView, AssignTicketView, AddTicketUpdateView

urlpatterns = [
    path('tickets/create/', CreateTicketView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/assign/', AssignTicketView.as_view(), name='ticket-assign'),
path('tickets/<int:pk>/update/', AddTicketUpdateView.as_view(), name='ticket-add-update'),
]