from fastapi import HTTPException

from internal.redis.cache import cache
from internal.redis.redis import redis_client
from repo.task_repo import (
    repo_create_task, 
    repo_delete_task, 
    repo_get_all_tasks, 
    repo_get_task_by_id, 
    repo_update_task
    )
from internal.celery.tasks import send_task_created_notification
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.task_schema import TaskRead

async def service_create_task(session: AsyncSession, user_id: int, title: str, description: str, completed: bool):
    task = await repo_create_task(session, user_id, title, description, completed)
    send_task_created_notification.delay(
        task.id,
        task.title
    )
    await redis_client.flushdb()
    return task

@cache(ttl=60)
async def service_get_all_tasks(session: AsyncSession, user_id, limit, offset):
    tasks = await repo_get_all_tasks(session, user_id, limit, offset)

    return [
        TaskRead.model_validate(task).model_dump(
            mode="json"
        )
        for task in tasks
    ]

async def service_delete_task(session: AsyncSession, task_id: int, user_id:int):
    task = await repo_delete_task(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    await redis_client.flushdb()
    return task

async def service_get_task_by_id(session: AsyncSession, task_id: int, user_id:int):
    task = await repo_get_task_by_id(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task

async def service_update_task(session: AsyncSession, task_id: int, title:str, description: str, completed: bool, user_id:int):
    task = await repo_update_task(session, task_id, title, description, completed, user_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    await redis_client.flushdb()
    
    return task