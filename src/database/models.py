from fileinput import filename
from django.db import models
import os


class Data(models.Model):
    uid = models.CharField(max_length=36, unique=True, primary_key=True)
    location = models.CharField(max_length=255, null=True)
    filename = models.CharField(max_length=255, null=True)

    def delete(self, *args, **kwargs):
        os.system("rm -rf " + self.location)
        super(Data, self).delete(*args, **kwargs)


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

    data = models.ForeignKey(
        to='Data',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Mail(models.Model):
    uid = models.CharField(max_length=36, unique=True, primary_key=True)
    mail = models.CharField(max_length=320)
