from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.user import User
from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate
from app.dependencies.permissions import check_task_permission

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

    async def create_task(
        self,
        task: TaskCreate,
        current_user: User,
    ):
        new_task = Task(
            title=task.title,
            description=task.description,
            created_by=current_user.id,
        )

        return await task_repository.create(
            self.db,
            new_task,
        )

    async def update_task(
    self,
    task_id: int,
    task: TaskUpdate,
    current_user: User,
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
        check_task_permission(
        current_user,
        db_task,
        )

        db_task.title = task.title
        db_task.description = task.description

        return await task_repository.update(
            self.db,
            db_task,
        )

    async def delete_task(
        self,
        task_id: int,
        current_user: User,
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
        check_task_permission(
            current_user,
            db_task,
        )

        await task_repository.delete(
            self.db,
            db_task,
        )

        return