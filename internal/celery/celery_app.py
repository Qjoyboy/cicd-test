from celery import Celery

celery_app = Celery(
    "todo",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)
celery_app.conf.task_always_eager = False
import internal.celery.tasks