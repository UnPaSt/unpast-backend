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
    import subprocess
    #FIXME pathing issue of dependent R script
    subprocess.run(["python3",
                    "DESMOND2/run_desmond.py" "--exprs" "data/TCGA_200.exprs_z.tsv" "--basename" "TCGA_200" "-p"" 0.001" "--seed" "800691" "-c" "WGCNA"])
