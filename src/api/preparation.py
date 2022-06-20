import json
import os
import uuid
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDict
from rest_framework.request import Request

from database.models import Task


def get_uid_for_file():
    uid = str(uuid.uuid4())
    while Task.objects.filter(uid=uid).exists():
        uid = str(uuid.uuid4())
    return uid


def get_wd(uid):
    return os.path.join("/tmp", uid) + "/"


def get_matrix_path(uid):
    return os.path.join(get_wd(uid), uid + ".matrix")


def save_task(uid, request :Request):
    os.mkdir(get_wd(uid))
    write_file(uid, request.FILES.get('file'))
    Task.objects.create(uid=uid, status="Initialized")


def write_file(uid, file):
    print(file)
    fs = FileSystemStorage(location=get_wd(uid))
    filename = fs.save(file.name, file)
    # fs.url(filename)
    os.system("mv " + os.path.join(get_wd(uid), filename) + " " + get_matrix_path(uid))


def update_task(uid, req) -> Task:
    task = Task.objects.get(uid=uid)
    task.request = json.dumps(req)
    task.status = "Ready"
    task.save()
    return task
