from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from employee_website import *


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aditshsoft.settings')

app = Celery('aditshsoft')
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-report-every-single-minute': {
        'task': 'employee_website.tasks.auto_escalation_resume_receipt',
        'schedule': 1.0,
    },
}
