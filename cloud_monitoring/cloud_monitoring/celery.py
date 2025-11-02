import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_monitoring.settings')
app = Celery('cloud_monitoring')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()