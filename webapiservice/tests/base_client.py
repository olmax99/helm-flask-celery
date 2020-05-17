import pytest

# from flaskapi.core import database
# from flaskapi.core.redis_config import DecodedRedis
# from flaskapi.core.redis_conn import FlaskRedis

# test_redis = FlaskRedis.from_custom_provider(
#     DecodedRedis, app=None, config_prefix='TEST_REDIS')


# @pytest.fixture(scope='session')
# def client():
#     app = api.create_app(config='Testing')
#     client = app.test_client()
#
#     with app.app_context():
#         # database.init_db()
#         test_redis.init_app(app)
#
#     yield client


@pytest.fixture(scope='session')
def celery_app():
    from core.celery_conn import celery
    # for use celery_worker fixture
    from celery.contrib.testing import tasks  # NOQA
    return celery
