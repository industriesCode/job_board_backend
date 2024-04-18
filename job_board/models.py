from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    """
        This model represents job listings within the application. It stores information such as the company name, job
        title, description, location, experience required, and the user who created the job. Additionally, it keeps
        track of users who have applied for the job.

        Dependencies:
            models: Module within Django for defining database models.
            django.contrib.auth.models.User: Django's built-in User model for user authentication and management.
    """
    company = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    experience = models.IntegerField(null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(User, related_name='applied_jobs', blank=True)

    def __str__(self):
        return self.title

