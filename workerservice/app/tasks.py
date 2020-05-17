# ------------------------------------------------------------------------------------
#   TASKS ARE SPLIT INTO TWO DIFFERENT QUEUES:
#       1. Default Queue: executes all reoccurring periodic beat tasks
#       2. Background Queue: meant to execute CPU heavy non-blocking tasks
#
# ------------------------------------------------------------------------------------
import os
import time
import datetime


from celery.utils.log import get_task_logger
from celery_conn import make_celery

app = make_celery()

logger = get_task_logger(__name__)


@app.task(name='tasks.see_you')
def see_you(arg):
    t = datetime.datetime.now()
    logger.info(f"See you in ten seconds, {arg}!")
    return f"FINISHED {t}"


@app.task(name='tasks.longcompute', queue='background')
def make_long_compute(new_job_uuid, sync_runner_job_id, called_at):
    logger.info(f"[called at] {called_at}. Start long compute task {new_job_uuid} ...")
    time.sleep(10)
    logger.info(f"Long compute {sync_runner_job_id} just FINISHED.")
    return "Test: COMPUTE FINISHED."
