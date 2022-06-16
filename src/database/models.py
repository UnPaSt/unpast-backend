from django.db import models


class Task(models.Model):
    uid = models.CharField(max_length=36, unique=True, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)

    has_matrix = models.BooleanField(default=False)
    status = models.CharField(max_length=255, null=True)

    done = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    result = models.TextField(null=True)