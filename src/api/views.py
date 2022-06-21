import json
import os

from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from database.models import *
from .preparation import get_uid_for_file, save_task, get_wd, update_task, store_mail


@api_view(['POST'])
@csrf_exempt
@parser_classes([MultiPartParser])
def upload_matrix(req) -> Response:
    if req.method == 'POST':
        uid = get_uid_for_file()
        save_task(uid, req)
        return Response({"id": uid})
    return Response()


@api_view(['GET'])
def remove_matrix(req) -> Response:
    try:
        uid = req.GET.get("id")
        task: Task = Task.objects.get(uid=uid)
        task.delete()
        os.system("rm -rf " + get_wd(uid))
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({"id": uid}, status=status.HTTP_200_OK)


@api_view(['POST'])
def run_task(req) -> Response:
    from .queue import queue_task
    params = req.data
    uid = params["id"]
    try:
        mail = None if "mail" not in params else params["mail"]
        task = update_task(uid, params)
        store_mail(uid, mail)
        queue_task(task)
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({"id": uid}, status=status.HTTP_200_OK)


def get_task_status(uid):
    status = {"id": uid}
    task = Task.objects.get(uid=uid)
    status["status"] = task.status
    status["query"] = json.loads(task.request)
    if task.error:
        task.error = True
        return status
    status["done"] = task.done
    if task.done:
        status["result"] = json.loads(task.result)
    return status


@never_cache
@api_view(['GET'])
def get_task(req) -> Response:
    uid = req.GET.get("id")
    return Response(get_task_status(uid))
