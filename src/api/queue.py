import worker.tasks.background


def queue_task(task):
    worker.tasks.background.desmond2_job.delay(task.uid)
    task.status = "Queued"
    task.save()
