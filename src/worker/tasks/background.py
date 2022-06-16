from worker.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task(name='test-job')
def test_job():
    logger.info("Running job")
    import time
    time.sleep(10)
    logger.info("Done")
    return {"done": True}


@app.task(name='desmond2-run')
def desmond2_job():
    logger.info("Started Desmond2 execution")
    from DESMOND2.run_desmond import run_DESMOND
    run_DESMOND("/usr/src/desmond2/data/TCGA_200.exprs_z.tsv", "/usr/src/desmond2/data/TCGA_200_detached", save=True, load=False, clust_method='Louvain', cluster_binary=False, seed=800691)
    logger.info("Done")
