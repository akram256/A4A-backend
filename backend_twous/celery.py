from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_twous.settings.local')

app = Celery('backend_twous')

app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'display_time-30-seconds': {
        'task': 'demoapp.tasks.display_time',
        'schedule': 10.0
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))