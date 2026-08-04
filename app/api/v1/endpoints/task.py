from typing import List

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Query,
    Response,
    status,
)

from app.dependencies.auth import get_current_user
from app.dependencies.task import get_task_service
from app.models.task_enum import (
    TaskPriority,
    TaskStatus,
)
from app.models.user import User
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.services.task_service import TaskService

router = APIRouter(
    tags=["Tasks"],
)


@router.get(
    "/projects/{project_id}/tasks",
    response_model=List[TaskResponse],
)
async def get_project_tasks(
    project_id: int,
    task_status: TaskStatus | None = Query(
        default=None,
        alias="status",
    ),
    priority: TaskPriority | None = Query(
        default=None,
    ),
    assignee_id: int | None = Query(
        default=None,
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    return await service.get_tasks(
        project_id=project_id,
        current_user=current_user,
        status_filter=task_status,
        priority=priority,
        assignee_id=assignee_id,
        page=page,
        limit=limit,
    )


@router.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project_task(
    project_id: int,
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(
        project_id=project_id,
        task=task,
        current_user=current_user,
        background_tasks=background_tasks,
    )


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    return await service.get_task(
        task_id=task_id,
        current_user=current_user,
    )


@router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    return await service.update_task(
        task_id=task_id,
        task=task,
        current_user=current_user,
        background_tasks=background_tasks,
    )


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    await service.delete_task(
        task_id=task_id,
        current_user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )