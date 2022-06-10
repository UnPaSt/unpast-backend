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