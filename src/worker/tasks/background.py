import json
import os
from datetime import datetime

from worker.celery import app
from celery.utils.log import get_task_logger

from database.messenger import error_notification

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
    params = json.loads(task.request)

    bin_method = 'GMM' if 'binarization' not in params else params['binarization']
    clust_method = 'Louvain' if 'clustering' not in params else params['clustering']
    seed = 42 if 'seed' not in params else params["seed"]
    pval = 0.001 if 'pval' not in params else params["pval"]
    r = 0.3 if 'r' not in params else params["r"]
    try:
        from app import run_desmond
        result = run_desmond.run_DESMOND(exprs_file=get_matrix_path(uid), basename=os.path.join(get_wd(uid),uid),
                                         verbose=False, save=True, load=False, clust_method=clust_method,
                                         cluster_binary=False, bin_method=bin_method, seed=seed, pval=pval, r=r)
        task.finished_at = datetime.now()
        task.status = "Finishing"
        task.save()
    except Exception as e:
        task.error = True
        task.status = f'DESMOND2 execution {uid} exited with an error: {e}'
        task.save()
        error_notification(f'DESMOND2 execution {uid} exited with an error: {e}')
        logger.info(task.status)
        return
    task.result = result.to_json(orient='index')
    task.done = True
    task.status = "Done"
    task.save()
    logger.info(f"DESMOND2 execution {uid} finished!")
