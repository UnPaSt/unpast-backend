import json
import os
import mimetypes

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http.response import HttpResponse

from database.models import *
from .preparation import get_uid, save_file, update_task, store_mail, get_formatted_input


def download_example(request):
    # Define text file name
    filename = 'TCGA_200.exprs_z.tsv'
    # Define the full file path
    filepath = os.path.join('data', filename)
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


@api_view(['POST'])
@csrf_exempt
@parser_classes([MultiPartParser])
def upload_matrix(req) -> Response:
    if req.method == 'POST':
        uid = get_uid(Data)
        save_file(uid, req)
        return Response({"id": uid})
    return Response()


@api_view(['GET'])
def remove_matrix(req) -> Response:
    try:
        uid = req.GET.get("id")
        data: Data = Data.objects.get(uid=uid)
        data.delete()
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({"id": uid}, status=status.HTTP_200_OK)


@api_view(['GET'])
def remove_task(req) -> Response:
    try:
        uid = req.GET.get("id")
        task: Task = Task.objects.get(uid=uid)
        data = task.data
        task.delete()
        # remove file if it is not assigned to any task anymore
        if (data is not None) and (not data.task_set.all()):
            data.delete()
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({"id": uid}, status=status.HTTP_200_OK)


@api_view(['POST'])
def run_task(req) -> Response:
    from .queue import queue_task
    params = req.data
    file_uid = params["id"]
    try:
        data: Data = Data.objects.get(uid=file_uid)
        task_uid = get_uid(Task)
        Task.objects.create(
            uid=task_uid,
            status="Initialized",
            request=json.dumps({}),
            data=data)
        mail = None if "mail" not in params else params["mail"]
        task = update_task(task_uid, params)
        store_mail(task_uid, mail)
        queue_task(task)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({"id": task_uid}, status=status.HTTP_200_OK)


def get_task_status(uid, append_result=True):
    status = {"id": uid}
    task = Task.objects.get(uid=uid)
    status["status"] = task.status
    status["query"] = json.loads(task.request)
    status["query"]["exprs"] = task.data.filename if task.data is not None else ''
    status["created"] = task.created_at.timestamp()
    if task.error:
        task.error = True
        return status
    status["done"] = task.done
    if task.done and append_result:
        status["result"] = json.loads(task.result)
    return status


@never_cache
@api_view(['GET'])
def get_task_data(req) -> Response:
    uid = req.GET.get("id")
    try:
        task = Task.objects.get(uid=uid)
        data = False
        if task.data is not None:
            data = get_formatted_input(task.data, json.loads(task.result))
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response(data, status=status.HTTP_200_OK)


@never_cache
@api_view(['GET'])
def get_task(req) -> Response:
    uid = req.GET.get("id")
    return Response(get_task_status(uid))


@never_cache
@api_view(['POST'])
def get_task_statuses(req) -> Response:
    statuses = []
    for uid in req.data.get("ids"):
        statuses.append(get_task_status(uid, append_result=False))
    return Response(statuses)
