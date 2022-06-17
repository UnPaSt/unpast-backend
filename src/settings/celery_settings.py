import os
# Looks up for task modules in Django applications and loads them

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL','redis://desmond2_broker:6379/0')
CELERY_TIMEZONE = 'Europe/Berlin'

CELERY_BROKER_USER = os.environ.get('RABBITMQ_DEFAULT_USER')
CELERY_BROKER_PASSWORD = os.environ.get('RABBITMQ_DEFAULT_PASS')

CELERY_BEAT_SCHEDULE = {
    'cleaner': {
        'task': 'worker.tasks.housekeeping.clean_tasks',
        'schedule': 60.0
    }
}

