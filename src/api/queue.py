import worker.tasks.background

def queue_test_job(clust):
    worker.tasks.background.desmond2_job.delay(clust)
    return {"done": True}
