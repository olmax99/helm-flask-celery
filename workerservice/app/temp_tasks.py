# from celery import shared_task


from app.celery_conn import make_celery

app = make_celery()


@app.task(name='tasks.mul', queue='background')
def mul(x, y):
    return x * y
