from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    company = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    experience = models.IntegerField(null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    applicants = models.ManyToManyField(User, related_name='applied_jobs', blank=True)

    def __str__(self):
        return self.title

