import os
from datetime import datetime

from celery import shared_task

from settings import settings


def get_wd(uid):
    return os.path.join("/tmp", uid) + "/"


def is_too_old(ts):
    if (datetime.utcnow() - ts.replace(tzinfo=None)).total_seconds() > settings.MATRIX_CACHE_DURATION:
        return True
    return False


@shared_task
def clean_tasks():
    from database.models import Task
    for t in Task.objects.filter(started_at__isnull=True):
        if is_too_old(t.created_at):
            os.system(f"rm -rf {get_wd(t.uid)}")
            t.delete()


@shared_task
def send_notifications():
    from database.messenger import error_notification, send_notification
    from database.models import Mail, Task

    for mail in Mail.objects.all():
        try:
            task = Task.objects.get(uid=mail.uid)
            if task.done:
                send_notification(mail.mail, False, mail.uid)
                mail.delete()
            elif task.error:
                send_notification(mail.mail, True)
                mail.delete()
        except Exception as e:
            error_notification(f"Task for mail {mail.mail} of task {mail.uid} could not be found: {e}")
            mail.delete()
