import os
import uuid
from database.models import Task


def get_uid_for_file():
    uid = uuid.uuid4()
    print(Task.objects.get(uid=uid))
    while Task.objects.get(uid=uid):
        uid = uuid.uuid4()
    return uid


def set_uid(data):
    data["uid"] = str(get_uid_for_file())
    data["out"] = os.path.join("/tmp", str(data["uid"])) + "/"
    os.mkdir(data["out"])