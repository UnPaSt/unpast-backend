from django.urls import path
from .views import run_task, upload_matrix, remove_matrix, get_task

urlpatterns = [
    path('upload_matrix',upload_matrix),
    path('remove_matrix',remove_matrix),
    path('run_task',run_task),
    path('get_task',get_task)
]
