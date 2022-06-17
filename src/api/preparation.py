import os
import uuid
from datetime import datetime

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


def save_task(uid, req):
    os.mkdir(get_wd(uid))
    # TODO replace with real file content once ready
    # write_file(get_matrix_path(uid), file)
    os.system('cp data/TCGA_200.exprs_z.tsv ' + get_matrix_path(uid))
    Task.objects.create(uid=uid)


def write_file(path, file):
    with open(path, "w") as fh:
        for line in file.split("\n"):
            fh.write(line)
