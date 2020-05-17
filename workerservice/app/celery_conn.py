import os

from celery import Celery

import celery_config


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://:super_secret_redis_from_secret@localhost:6379/0'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://:super_secret_redis_from_secret@localhost:6379/0')


def make_celery():
    app = Celery(broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['tasks'])
    # app.conf.update(app.config)
    app.config_from_object(celery_config)
    return app
