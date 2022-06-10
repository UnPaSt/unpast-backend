from django.urls import path
from .views import test_job

urlpatterns = [
    path('test',test_job)
]
