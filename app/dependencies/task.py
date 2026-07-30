from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.services.task_service import TaskService


def get_task_service(
    db: AsyncSession = Depends(get_db),
):
    return TaskService(db)