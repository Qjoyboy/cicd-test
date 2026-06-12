from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from internal.db.session import get_db
from internal.models.user_model import User
from internal.security.dependencies import get_current_user
from service.task_service import (
    service_create_task,
    service_delete_task,
    service_get_all_tasks,
    service_get_task_by_id,
    service_update_task
)
from schemas.task_schema import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

DBConn = Annotated[AsyncSession, Depends(get_db)]

@router.post("/", response_model=TaskRead)
async def create_task(session: DBConn, task: TaskCreate, current_user: User = Depends(get_current_user)):
    return await service_create_task(session,current_user.id, task.title, task.description, task.completed)

@router.get("/", response_model=List[TaskRead])
async def get_all_tasks(
    session: DBConn,
    current_user: User = Depends(get_current_user),
    limit: int = Query(default = 10, le=100),
    offset: int = 0
    ):
    return await service_get_all_tasks(session, current_user.id, limit, offset)

@router.get("/{task_id}",response_model=TaskRead)
async def get_task_by_id(session: DBConn, task_id: int, current_user: User = Depends(get_current_user)):
    return await service_get_task_by_id(session, task_id,current_user.id)

@router.delete("/{task_id}")
async def delete_task(session: DBConn, task_id: int, current_user: User = Depends(get_current_user)):
    return await service_delete_task(session, task_id,current_user.id)

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(session: DBConn, task:TaskUpdate, task_id: int, current_user: User = Depends(get_current_user)):
    return await service_update_task(session, task_id, task.title, task.description, task.completed,current_user.id)