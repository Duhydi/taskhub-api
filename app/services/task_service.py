import json
from datetime import datetime

from fastapi import (
    BackgroundTasks,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.background.email import send_assign_email
from app.core.redis import (
    clear_task_cache,
    redis_client,
)
from app.dependencies.permissions import (
    check_task_permission,
)
from app.models.task import Task
from app.models.task_enum import (
    TaskPriority,
    TaskStatus,
)
from app.models.user import User
from app.repositories import task_repository
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.repositories.user import UserRepository
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
)


class TaskService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.user_repo = UserRepository(db)

    async def get_tasks(
        self,
        project_id: int,
        status_filter: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assignee_id: int | None = None,
        page: int = 1,
        limit: int = 10,
    ):
        await self._get_project_or_404(
            project_id
        )

        cache_key = (
            f"project:{project_id}:tasks:"
            f"{status_filter}:{priority}:"
            f"{assignee_id}:{page}:{limit}"
        )

        cached = await redis_client.get(
            cache_key
        )

        if cached is not None:
            return json.loads(cached)

        tasks = await task_repository.get_by_project(
            self.db,
            project_id=project_id,
            status=status_filter,
            priority=priority,
            assignee_id=assignee_id,
            page=page,
            limit=limit,
        )

        data = [
            self._serialize_task(task)
            for task in tasks
        ]

        await redis_client.set(
            cache_key,
            json.dumps(data),
            ex=60,
        )

        return tasks

    async def get_task(
        self,
        task_id: int,
    ):
        task = await task_repository.get_by_id(
            self.db,
            task_id,
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task

    async def create_task(
        self,
        project_id: int,
        task: TaskCreate,
        current_user: User,
        background_tasks: BackgroundTasks,
    ):
        await self._get_project_or_404(
            project_id
        )

        assignee = None

        if task.assignee_id is not None:
            assignee = await self.user_repo.get_by_id(
                task.assignee_id
            )

            if assignee is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assignee not found",
                )

        new_task = Task(
            project_id=project_id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            assignee_id=task.assignee_id,
            due_date=task.due_date,
            created_by=current_user.id,
        )

        created_task = await task_repository.create(
            self.db,
            new_task,
        )

        await clear_task_cache(
            project_id
        )

        if assignee is not None:
            background_tasks.add_task(
                send_assign_email,
                assignee.email,
                created_task.title,
            )

        return created_task

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

        update_data = task.model_dump(
            exclude_unset=True,
        )

        old_assignee_id = db_task.assignee_id

        if "assignee_id" in update_data:
            new_assignee_id = update_data[
                "assignee_id"
            ]

            if new_assignee_id is not None:
                assignee = await self.user_repo.get_by_id(
                    new_assignee_id
                )

                if assignee is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Assignee not found",
                    )

        for field, value in update_data.items():
            setattr(
                db_task,
                field,
                value,
            )

        updated_task = await task_repository.update(
            self.db,
            db_task,
        )

        await clear_task_cache(
            db_task.project_id
        )

        return updated_task

    async def delete_task(
        self,
        task_id: int,
        current_user: User,
    ) -> None:
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

        project_id = db_task.project_id

        await task_repository.delete(
            self.db,
            db_task,
        )

        await clear_task_cache(
            project_id
        )

    async def _get_project_or_404(
        self,
        project_id: int,
    ):
        project = await self.project_repo.get_by_id(
            project_id
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project

    @staticmethod
    def _serialize_task(
        task: Task,
    ) -> dict:
        return {
            "id": task.id,
            "project_id": task.project_id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "priority": task.priority.value,
            "created_by": task.created_by,
            "assignee_id": task.assignee_id,
            "due_date": (
                task.due_date.isoformat()
                if task.due_date
                else None
            ),
            "created_at": (
                task.created_at.isoformat()
                if task.created_at
                else None
            ),
            "updated_at": (
                task.updated_at.isoformat()
                if task.updated_at
                else None
            ),
        }