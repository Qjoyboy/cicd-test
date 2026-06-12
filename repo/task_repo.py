from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from internal.models.task_model import Task

async def repo_create_task(
        session: AsyncSession, 
        user_id: int,
        title: str,
        description: str,
        completed: bool,
        ):
    task = Task(title=title, description=description, completed=completed, user_id=user_id)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def repo_get_all_tasks(
        session: AsyncSession, 
        user_id:int,
        limit:int,
        offset: int
        ):
    tasks = await session.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .limit(limit)
        .offset(offset)
    )
    return tasks.scalars().all()

async def repo_get_task_by_id(session: AsyncSession, task_id: int, user_id: int):
    task = await session.execute(
        select(Task).where(Task.id==task_id, Task.user_id==user_id)
    )

    return task.scalar_one_or_none()

async def repo_delete_task(session: AsyncSession, task_id: int, user_id: int):
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id==user_id)
    )

    task = result.scalar_one_or_none()

    if not task:
        return None
    
    await session.delete(task)
    await session.commit()

    return {"Masage": "gud"}

async def repo_update_task(
        session: AsyncSession, 
        task_id: int,
        title: str | None,
        description: str | None,
        completed: bool | None,
        user_id: int
        ):
    res = await session.execute(
        select(Task).where(Task.id==task_id, Task.user_id==user_id)
    )
    task = res.scalar_one_or_none()

    if not task:
        return None
    
    if title is not None:
        task.title = title

    if description is not None:
        task.description = description
    
    if completed is not None:
        task.completed = completed
    
    await session.commit()
    await session.refresh(task)

    return task