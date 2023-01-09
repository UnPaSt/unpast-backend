import worker.tasks.background


def queue_task(task):
    worker.tasks.background.unpast_job.delay(task.uid)
    task.status = "Queued"
    task.save()
