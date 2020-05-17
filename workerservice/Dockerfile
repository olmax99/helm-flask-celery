FROM python:3.6-stretch AS builder

## install dependencies for psycopg2
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends gcc

## add and install requirements
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# --------------------------------------------------------------------------------------
#   Worker Setup
# --------------------------------------------------------------------------------------

FROM python:3.6-stretch
COPY --from=builder /root/.local /root/.local

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
    && rm -rf /var/lib/apt/lists/*

# Custom Supervisord config
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

## add app
COPY . /usr/src/queue

## add user
#RUN addgroup --system user1 && adduser --system --no-create-home --group user1
#RUN chown -R user1:user1 /usr/src/app && chmod -R 755 /usr/src/app

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH=/root/.local/bin:$PATH

WORKDIR /usr/src/queue/app

## SCHEDULER BUILT
# ENTRYPOINT celery beat --app=tasks.app beat --loglevel=INFO

## BACKGROUND QUEUE
## pool gevent --concurrency=200: execute thousands of non-blocking requests for I/O-bound (e.g. HTTP)
## pool prefork: execute Kernel-bound processes for CPU (e.g. calculation)
# ENTRYPOINT celery worker --app=tasks.app --pool=prefork --queues=background --loglevel=INFO

# DEFAULT PERIODIC BEAT QUEUE
# pool solo: managing the k8s worker pool rather than managing multiple execution pools
# ENTRYPOINT celery worker --app=tasks.app --pool=solo --loglevel=INFO
