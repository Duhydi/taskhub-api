from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


async def get_all(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()


async def get_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, task: Task):
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def update(db: AsyncSession, task: Task):
    await db.commit()
    await db.refresh(task)
    return task


async def delete(db: AsyncSession, task: Task):
    await db.delete(task)
    await db.commit()