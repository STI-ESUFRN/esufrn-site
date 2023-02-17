from __future__ import absolute_import

import os

from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esufrn.settings")
app = Celery(
    "esufrn",
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

logger = get_task_logger(__name__)
