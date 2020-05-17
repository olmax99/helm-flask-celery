import os


class Config(object):
    DEBUG = False
    TESTING = False
    # DATABASE_URI = 'sqlite:///:memory:'


# TODO: Production will be configured along with CloudFormation
# class ProductionConfig(Config):
#     # DATABASE_URI = 'mysql://user@localhost/foo'
#     pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

    # OPTIONALLY: PostgreSQL
    # SQLALCHEMY_DATABASE_URI: str = os.getenv('POSTGRES_URI', None)
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # REDIS_HOST: str = os.getenv('REDIS_HOST', 'redis')
    # REDIS_PASSWD: str = os.getenv('REDIS_PASSWD', None)
    REDIS_URI: str = os.getenv('CELERY_BROKER_URL', None)


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    # SQLALCHEMY_DATABASE_URI: str = f"postgresql+psycopg2://test:test123@postgres.testing/test_api"
    # TEST_REDIS_URI: str = "redis://:super_secret_redis_from_secret@localhost:6379/0"
