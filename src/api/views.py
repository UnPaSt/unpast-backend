import os

from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from database.models import *
from .preparation import get_uid_for_file, save_task, get_wd


@never_cache
@api_view(['GET'])
def test_job(req) -> Response:
    clust = req.GET.get('clust')
    print("test route")
    from .queue import queue_test_job
    queue_test_job(clust)
    return Response()


@api_view(['POST'])
def upload_matrix(req) -> Response:
    uid = get_uid_for_file()
    save_task(uid, req)
    return Response({"id": uid})


@api_view(['GET'])
def remove_matrix(req) -> Response:
    try:
        uid = req.GET.get("id")
        task: Task = Task.objects.get(uid=uid)
        task.delete()
        os.system("rm -rf "+get_wd(uid))
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response({}, status=status.HTTP_200_OK)
