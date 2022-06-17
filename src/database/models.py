from django.db import models


class Task(models.Model):
    uid = models.CharField(max_length=36, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    status = models.CharField(max_length=255, null=True)

    done = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    request = models.TextField(null=True)
    result = models.TextField(null=True)