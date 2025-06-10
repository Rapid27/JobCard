from django.db import models
from django.utils import timezone

class JobCard(models.Model):
    CATEGORY_CHOICES = [
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('carpentry', 'Carpentry'),
        ('building', 'Building'),
        ('painting', 'Painting'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('awaiting_spares', 'Awaiting Spares'),
        ('done', 'Done'),
    ]

    location = models.CharField(max_length=255)
    work_required = models.TextField()
    reported_by = models.CharField(max_length=100)
    department_of_reporter = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    time_submitted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category.title()} - {self.location} - {self.status.title()}"
