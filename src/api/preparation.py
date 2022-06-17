import json
import os
import uuid
from datetime import datetime

from django.core.files.storage import FileSystemStorage
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

    print(request.POST)
    print(request.FILES)
    os.mkdir(get_wd(uid))
    # TODO replace with real file content once ready
    # write_file(get_matrix_path(uid), file)
    os.system('cp data/TCGA_200.exprs_z.tsv ' + get_matrix_path(uid))
    Task.objects.create(uid=uid, status="Initialized")


def write_file(path, file):
    with open(path, "w") as fh:
        for line in file.split("\n"):
            fh.write(line)


def update_task(uid, req) -> Task:
    task = Task.objects.get(uid=uid)
    task.request = json.dumps(req)
    task.status = "Ready"
    task.save()
    return task
