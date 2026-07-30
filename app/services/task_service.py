from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate

from fastapi import HTTPException, status

class TaskService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks(self):
        return await task_repository.get_all(self.db)

    async def get_task(self, task_id: int):
        return await task_repository.get_by_id(
            self.db,
            task_id,
        )

    async def create_task(self, task: TaskCreate):
        new_task = Task(
            title=task.title,
            description=task.description,
        )

        return await task_repository.create(
            self.db,
            new_task,
        )

    async def update_task(
        self,
        task_id: int,
        task: TaskUpdate,
    ):
        db_task = await task_repository.get_by_id(
            self.db,
            task_id,
        )

        if db_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        db_task.title = task.title
        db_task.description = task.description

        return await task_repository.update(
            self.db,
            db_task,
        )

    async def delete_task(self, task_id: int):
        db_task = await task_repository.get_by_id(
            self.db,
            task_id,
        )

        if db_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        await task_repository.delete(
            self.db,
            db_task,
        )

        return