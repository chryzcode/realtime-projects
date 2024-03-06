import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_init.settings')
app = Celery('init_app', broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BROKER_URL)
# app.conf.broker_url = settings.CELERY_BROKER_URL
app.config_from_object('celery_init.settings', namespace='CELERY')
# Load tasks from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')