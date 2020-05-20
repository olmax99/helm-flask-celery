"""
All tests assume that the tasks have been successfully delivered to the
 appropriate queue.

 Pytest will trigger the tasks instead of the endpoint

1. Test the
for details view:
  - https://docs.celeryproject.org/en/latest/userguide/testing.html#py-test?


"""

import logging
import time

from celery.result import ResultBase

from app import tasks


def test_see_you(caplog, celery_app, celery_session_worker):
    # celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
    with caplog.at_level(logging.DEBUG):
        logger = logging.getLogger()

        task = tasks.see_you.delay('test')
        logger.debug(f"SEE_YOU TASK: {task}, {type(task)}")
        response = task.wait(timeout=20, interval=5)

    assert response[:8] == 'FINISHED'


def test_make_long_compute(caplog, celery_app, celery_session_worker):
    with caplog.at_level(logging.DEBUG):
        logger = logging.getLogger()

        task = celery_app.send_task(
            'tasks.longcompute',
            args=['string1',
                  'string2',
                  'string3'],
            kwargs={}
        )
        # task = tasks.make_long_compute.delay('string1', 'string2', 'string3')
        logger.debug(f"TASK_RESPONSE: {task}, {type(task)} \n"
                     f"TASK_ID: {task.id}, {type(task.id)}")
        response = task.wait(timeout=20, interval=5)

    assert response == 'Test: COMPUTE FINISHED.'
