from datetime import timedelta
from celery.schedules import crontab


CELERY_IMPORTS = ('tasks')
# CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'tasks.see_you',
        # Every minute
        # 'schedule': crontab(minute="*"),
        # Every 30 seconds
        "schedule": timedelta(seconds=30),
        "args": ["JOB"]
    }
}
