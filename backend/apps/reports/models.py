# apps/reports/models.py
from django.conf import settings
from django.db import models

class Report(models.Model):

    STATUS_CHOICES = [
        ('new', 'Nowe'),
        ('in_progress', 'W realizacji'),
        ('resolved', 'Rozwiązane'),
        ('rejected', 'Odrzucone'),
    ]

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-likes', '-created_at']

    def __str__(self):
        return f"Report {self.id} by {self.user} [{self.status}]"


class AdminComment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='admin_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on Report {self.report_id}"


class UserComment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='user_comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"UserComment by {self.author} on Report {self.report_id}"


class StatusChange(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='status_history')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['changed_at']
