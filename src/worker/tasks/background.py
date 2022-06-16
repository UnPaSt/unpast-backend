import os

from worker.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task(name='desmond2-run')
def desmond2_job(clust):
    logger.info("Started Desmond2 execution")
    from app import run_desmond
    run_desmond.run_DESMOND("/usr/src/desmond2/data/TCGA_200.exprs_z.tsv", "/usr/src/desmond2/data/TCGA_200_detached", verbose=False, save=True, load=False, clust_method=clust, cluster_binary=False, seed=800691)
    logger.info("Done")
