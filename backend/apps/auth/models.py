# auth/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('standard', 'Standard'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='standard')
    data = models.TextField(blank=True, null=True)
    # Lista ID raportów jako tablica JSON
    # inaczej?
    reports = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"