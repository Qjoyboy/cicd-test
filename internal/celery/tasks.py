from internal.celery.celery_app import celery_app
import time

@celery_app.task
def send_task_created_notification(task_id: int, title: str):
    print(f"Task created: id={task_id}, title={title}")