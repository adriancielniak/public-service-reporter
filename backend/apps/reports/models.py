# apps/reports/models.py
from django.conf import settings
from django.db import models

class Report(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        # to daje wirtualne odwrocenie relacji
        # szybko mozna znalezc wszystkie reporty usera
        related_name='reports'
    )
    content = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_reports',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-likes', '-created_at']

    def __str__(self):
        return f"Report {self.id} by {self.user}"
