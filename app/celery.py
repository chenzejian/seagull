import os
from celery import Celery
from django.conf import settings
from config import celeryconfig

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('ym-email')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(celeryconfig)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

autoretry_for=(Exception,)
short_default = app.task(
    autoretry_for=autoretry_for,
    default_retry_delay=1 * 6,
    retry_kwargs={
        'max_retries': 5,
    },
    # queue='celery',
    # base=YmTask
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))