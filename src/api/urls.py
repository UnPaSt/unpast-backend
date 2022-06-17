from django.urls import path
from .views import test_job, upload_matrix, remove_matrix

urlpatterns = [
    path('test',test_job),
    path('upload_matrix',upload_matrix),
    path('remove_matrix',remove_matrix)
]
