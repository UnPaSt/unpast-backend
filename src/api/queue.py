import worker.tasks.background

def queue_test_job():
    print("starting job detached")
    worker.tasks.background.test_job.delay()
    print("started job")
    return {"done": True}
