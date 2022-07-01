from django.urls import path
from .views import run_task, upload_matrix, remove_matrix, get_task, get_task_statuses, remove_task

urlpatterns = [
    path('upload_matrix',upload_matrix),
    path('remove_matrix',remove_matrix),
    path('remove_task',remove_task),
    path('run_task',run_task),
    path('get_task',get_task),
    path('get_task_statuses',get_task_statuses)
]
