import worker.tasks.background

def queue_test_job():
    worker.tasks.background.desmond2_job.delay()
    return {"done": True}
