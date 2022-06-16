from django.urls import path
from .views import test_job, upload_matrix

urlpatterns = [
    path('test',test_job),
    path('upload_matrix',upload_matrix)
]
