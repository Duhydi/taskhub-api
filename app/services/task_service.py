import json

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
from app.dependencies.permissions import check_task_permission
from app.models.task import Task
from app.models.task_enum import (
    TaskPriority,
    TaskStatus,
)
from app.models.user import User
from app.repositories import task_repository
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
)


class TaskService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks(
        self,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assignee_id: int | None = None,
        page: int = 1,
        limit: int = 10,
    ):
        print("Redis ping:", await redis_client.ping())

        cache_key = (
            f"tasks:{status}:{priority}:"
            f"{assignee_id}:{page}:{limit}"
        )

        cached = await redis_client.get(cache_key)

        if cached:
            print("✅ CACHE HIT")
            return json.loads(cached)

        print("❌ CACHE MISS")

        tasks = await task_repository.get_all(
            self.db,
            status=status,
            priority=priority,
            assignee_id=assignee_id,
            page=page,
            limit=limit,
        )

        data = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status.value,
                "priority": task.priority.value,
                "assignee_id": task.assignee_id,
            }
            for task in tasks
        ]

        await redis_client.set(
            cache_key,
            json.dumps(data),
            ex=60,
        )

        print("Saved:", cache_key)
        print("Redis Keys:", await redis_client.keys("*"))

        return tasks

    async def get_task(
        self,
        task_id: int,
    ):
        return await task_repository.get_by_id(
            self.db,
            task_id,
        )

    async def create_task(
        self,
        task: TaskCreate,
        current_user: User,
        background_tasks: BackgroundTasks,
    ):
        new_task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            assignee_id=task.assignee_id,
            created_by=current_user.id,
        )

        created_task = await task_repository.create(
            self.db,
            new_task,
        )

        await clear_task_cache()

        background_tasks.add_task(
            send_assign_email,
            current_user.email,
            created_task.title,
        )

        print("Cache cleared")
        print("Redis Keys:", await redis_client.keys("*"))

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

        db_task.title = task.title
        db_task.description = task.description
        db_task.status = task.status
        db_task.priority = task.priority
        db_task.assignee_id = task.assignee_id

        updated_task = await task_repository.update(
            self.db,
            db_task,
        )

        await clear_task_cache()

        print("Cache cleared")
        print("Redis Keys:", await redis_client.keys("*"))

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

        await task_repository.delete(
            self.db,
            db_task,
        )

        await clear_task_cache()

        print("Cache cleared")
        print("Redis Keys:", await redis_client.keys("*"))

        return None