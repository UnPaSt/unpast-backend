import os
from datetime import datetime

from celery import shared_task

from settings import settings

def get_wd(uid):
    return os.path.join("/tmp", uid) + "/"


def is_too_old(ts):
    if (datetime.utcnow()-ts.replace(tzinfo=None)).total_seconds() > settings.MATRIX_CACHE_DURATION:
        return True
    return False

@shared_task
def clean_tasks():
    from database.models import Task
    for t in Task.objects.filter(started_at__isnull=True):
        if is_too_old(t.created_at):
            print("Removing task: "+t.uid)
            os.system(f"rm -rf {get_wd(t.uid)}")
            t.delete()
