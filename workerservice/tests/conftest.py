import pytest

# Needed for celery_fixture to get registered - https://github.com/celery/celery/issues/4851
from celery.contrib.testing.tasks import ping

# You should override the celery_app fixture to use your app.
# See https://github.com/celery/celery/blob/master/celery/contrib/pytest.py#L164.


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://:super_secret_redis_from_secret@localhost:6379/0',
        'result_backend': 'redis://:super_secret_redis_from_secret@localhost:6379/0'
    }


@pytest.fixture()
def celery_app():
    from app.celery_conn import make_celery
    app_ = make_celery()

    return app_

