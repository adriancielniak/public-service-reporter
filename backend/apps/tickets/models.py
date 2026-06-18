# apps/tickets/models.py
from django.conf import settings
from django.db import models

#placeholder
class Ticket(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id}"