from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.task_enum import (
    TaskPriority,
    TaskStatus,
)


async def get_by_project(
    db: AsyncSession,
    project_id: int,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    assignee_id: int | None = None,
    page: int = 1,
    limit: int = 10,
):
    query = select(Task).where(
        Task.project_id == project_id
    )

    if status is not None:
        query = query.where(
            Task.status == status
        )

    if priority is not None:
        query = query.where(
            Task.priority == priority
        )

    if assignee_id is not None:
        query = query.where(
            Task.assignee_id == assignee_id
        )

    query = (
        query
        .order_by(Task.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await db.execute(query)

    return result.scalars().all()


async def get_by_id(
    db: AsyncSession,
    task_id: int,
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id
        )
    )

    return result.scalar_one_or_none()


async def get_by_id_and_project(
    db: AsyncSession,
    task_id: int,
    project_id: int,
):
    result = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.project_id == project_id,
        )
    )

    return result.scalar_one_or_none()


async def create(
    db: AsyncSession,
    task: Task,
):
    db.add(task)

    await db.commit()
    await db.refresh(task)

    return task


async def update(
    db: AsyncSession,
    task: Task,
):
    await db.commit()
    await db.refresh(task)

    return task


async def delete(
    db: AsyncSession,
    task: Task,
):
    await db.delete(task)
    await db.commit()