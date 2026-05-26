# Це гарантує, що Celery запуститься разом із Django
from .celery import app as celery_app

__all__ = ("celery_app",)
