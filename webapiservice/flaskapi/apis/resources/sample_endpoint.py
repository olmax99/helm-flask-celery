import json
import os
import uuid

from datetime import datetime

from flask import current_app
from flask_restx import Namespace, Resource

from flaskapi.core.celery_conn import celery
from celery.exceptions import TimeoutError, CeleryError
# from celery import group, chain

ns = Namespace('sample-namespace', description='A sample of various endpoints for testing.')


# TODO: Schema and request status handling (including exceptions!!)
@ns.route('/compute', endpoint='compute')
class SampleCompute(Resource):
    def get(self):
        """
        This is a sample compute task for verifying background jobs
        :return: <current job meta data>, response.code, response.header
        """

        with current_app.app_context():
            called_at = datetime.utcnow()
            new_job_uuid = str(uuid.uuid1())
            sync_runner_job_id = f"compute_{new_job_uuid}"

            try:
                res = celery.send_task('tasks.longcompute',
                                       queue='background',
                                       args=[new_job_uuid, sync_runner_job_id, called_at],
                                       kwargs={})
            except CeleryError as exc:
                raise exc
            except TimeoutError as exc:
                raise exc

            current_app.logger.info(f"WebApi: Send background job with id {res.id}.")

            # TODO: Use generic response implementation
            # Flask response standard: data or body, status code, and headers (default={'Content-Type': 'html'})
            return {'sync_runner_job_id': sync_runner_job_id,
                    'task': res.id,
                    'job_description': 'test: long compute',
                    'called_at': str(called_at),
                    }, 201, {'Content-Type': 'application/json'}


@ns.route('/<task_id>')
@ns.doc(params={'task_id': 'An ID'})
class JobCheck(Resource):
    def post(self, task_id):
        """
        Check the current state of a celery background task.
        TODO: result.forget() is required, but conflicts with idempotency
        :return:
        """
        with current_app.app_context():
            try:
                res = celery.AsyncResult(id=task_id)
            except CeleryError as exc:
                raise exc
            except TimeoutError as exc:
                raise exc

            result = res.get(timeout=2) if (res.state == 'SUCCESS') or \
                                           (res.state == 'FAILURE') else None

            return {"state": f"{res.state}",
                    "result": f"{result}"
                    }, 201, {'Content-Type': 'application/json'}

