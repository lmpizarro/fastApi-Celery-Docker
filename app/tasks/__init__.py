from celery import Celery
import logging

logger = logging.getLogger('celery tasks')


app = Celery('tasks', backend='redis://localhost', broker='redis://localhost//')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@app.task
def add(x, y):
    return x + y

