from celery import Celery
import logging
import json
import time
import redis

logger = logging.getLogger('celery tasks')

app = Celery('tasks', backend='redis://localhost', broker='redis://localhost//')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

pubsub_sus = redis.pubsub()
pubsub_sus.subscribe('fast_channel')

@app.task
def add(x, y):
    return x + y


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('world') every 30 seconds
    sender.add_periodic_task(1.0, receive_fast_channel.s(), name='receive_fast_channel every 1')

@app.task
def task_fast_channel(message):
    message = json.loads(message)
    logger.info(f'DOING THE HARD PART job_id {message["job_id"]} {message["data"]}')
    time.sleep(1)
    return f'END THE HARD PART job_id {message["job_id"]}'


@app.task
def receive_fast_channel():
    received = pubsub_sus.get_message()
    message = 'not message'
    if received != None:
        channel = received['channel'].decode('ascii')

        logger.info(f'channel {channel}')

        try:
            message = received["data"].decode('ascii')
            # reduce_time.delay(message)
            task_fast_channel.delay(message)
        except AttributeError as e:
            logger.error(f'decode message {e}')
    else:
        pass

    logger.info(f'received {message}')

    return 'BEAT RECEIVE_FAST_CHANNEL'

