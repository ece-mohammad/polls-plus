from django.db import models
from django.conf import settings
from pathlib import Path

# Create your models here.
class Project(models.Model):

    class MostRecentManager(models.Manager):

        def get_queryset(self):
            return super().get_queryset().order_by(
                "-created_at", "-updated_at"
            )[:settings.PROJECTS_RECENT_COUNT]


    class Meta:
        ordering = ["status", "-updated_at", "-created_at"]


    STATUS_CHOICES = [
        ('Live', 'Live'),
        ('Beta', 'Beta'),
        ('Development', 'Development'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to="projects/",
        null=True,
        blank=True
    )
    url = models.CharField(max_length=200)
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    docs_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    version = models.CharField(max_length=10)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    categories = models.JSONField(default=list)  # Store as JSON array
    technologies = models.JSONField(default=list)  # Store as JSON array
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    most_recent = MostRecentManager()

    def __str__(self):
        return self.title
