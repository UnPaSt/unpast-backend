import json
import os
from datetime import datetime

from worker.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def get_wd(uid):
    return os.path.join("/tmp", uid) + "/"


def get_matrix_path(uid):
    return os.path.join(get_wd(uid), uid + ".matrix")


@app.task(name='desmond2-run')
def desmond2_job(uid):
    from database.models import Task
    task = Task.objects.get(uid=uid)
    task.started_at = datetime.now()
    task.status = "Running"
    task.save()
    logger.info("Started Desmond2 execution of task " + uid)
    try:
        from app import run_desmond
        result = run_desmond.run_DESMOND(exprs_file=get_matrix_path(uid), basename=get_wd(uid),
                                         verbose=False, save=False, load=False, clust_method='Louvain',
                                         cluster_binary=False, seed=800691)
        task.finished_at = datetime.now()
        task.status = "Finishing"
        task.save()
    except Exception as e:
        task.error = True
        task.status = f'DESMOND2 execution {uid} exited with an error: {e}'
        task.save()
        logger.info(task.status)
        return
    task.result = result.to_json(orient='index')
    task.done = True
    task.status = "Done"
    task.save()
    logger.info(f"DESMOND2 execution {uid} finished!")
