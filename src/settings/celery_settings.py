import os
# Looks up for task modules in Django applications and loads them

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL','redis://desmond2_broker:6379/0')
CELERY_TIMEZONE = 'Europe/Berlin'

CELERY_BROKER_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
CELERY_BROKER_PASSWORD = os.environ.get('RABBITMQ_DEFAULT_PASS')


CELERY_BEAT_SCHEDULE = {
    # 'test_task': {
    #     'task': 'worker.tasks.default.run_test',
    #     'schedule': 10.0
    # }
}

