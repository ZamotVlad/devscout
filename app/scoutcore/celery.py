import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scoutcore.settings")

app = Celery("scoutcore")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
