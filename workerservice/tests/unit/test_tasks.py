"""
All tests assume that the tasks have been successfully delivered to the
 appropriate queue.

 Pytest will trigger the tasks instead of the endpoint

1. Test the
for details view:
  - https://docs.celeryproject.org/en/latest/userguide/testing.html#py-test?


"""


from app import tasks


def test_see_you(celery_app, celery_worker):
    assert tasks.see_you.delay('test').get(timeout=10)[:8] == 'FINISHED'
