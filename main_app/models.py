from django.db import models

STATUS_CHOICES = [
    ('REPORTED', 'Reported'),
    ('VERIFIED', 'Verified'),
    ('IN_PROGRESS', 'In Progress'),
    ('RESOLVED', 'Resolved'),
]

CATEGORY_CHOICES = [
    ('infra', 'Infrastruktur'),
    ('kebersihan', 'Kebersihan'),
    ('lingkungan', 'Lingkungan'),
    ('keamanan', 'Keamanan'),
    ('transportasi', 'Transportasi'),
]

class Report(models.Model):
    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()
    location = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='REPORTED'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title