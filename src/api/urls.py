from django.urls import path
from .views import run_task, upload_matrix, remove_matrix, get_task, get_task_statuses, remove_task, get_task_data, \
    download_example, server_status, get_result, get_log

urlpatterns = [
    path('upload_matrix',upload_matrix),
    path('remove_matrix',remove_matrix),
    path('remove_task',remove_task),
    path('run_task',run_task),
    path('get_task',get_task),
    path('get_task_data',get_task_data),
    path('get_task_statuses',get_task_statuses),
    path('download_example', download_example),
    path('server_status', server_status),
    path('get_result',get_result),
    path('get_log',get_log)
]
