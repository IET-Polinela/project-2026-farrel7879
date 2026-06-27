from django.conf import settings
from django.db import models


STATUS_CHOICES = [
    ("DRAFT", "Draft"),
    ("REPORTED", "Reported"),
    ("VERIFIED", "Verified"),
    ("IN_PROGRESS", "In Progress"),
    ("RESOLVED", "Resolved"),
]


CATEGORY_CHOICES = [
    ("infra", "Infrastruktur"),
    ("kebersihan", "Kebersihan"),
    ("lingkungan", "Lingkungan"),
    ("keamanan", "Keamanan"),
    ("transportasi", "Transportasi"),
    ("fasilitas_umum", "Fasilitas Umum"),
]


class Report(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports",
    )

    title = models.CharField(
        max_length=200,
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
    )

    description = models.TextField()

    location = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"