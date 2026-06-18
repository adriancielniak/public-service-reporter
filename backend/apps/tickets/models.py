from django.db import models
from django.conf import settings


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=255, blank=True, default='')  # odpowiednik 'treść' / opis skrócony
    description = models.TextField(blank=True, default='')  # pełna treść ticketu
    ticket_type = models.CharField(max_length=50, blank=True, default='')  # rodzaj
    created_at = models.DateTimeField(auto_now_add=True)  # data

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Przypisany użytkownik (worker/admin)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )

    # Lista stringow
    updates = models.JSONField(default=list, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"Ticket {self.id} [- {self.status} -]"