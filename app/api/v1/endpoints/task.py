from typing import List

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Query,
    Response,
    status,
)

from app.core.api_responses import (
    MUTATION_RESPONSES,
    RESOURCE_RESPONSES,
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
    summary="List project tasks",
    description=(
        "Return paginated tasks in a project. "
        "The result can be filtered by status, priority, "
        "and assignee. Task lists are cached in Redis."
    ),
    responses=RESOURCE_RESPONSES,
)
async def get_project_tasks(
    project_id: int,
    task_status: TaskStatus | None = Query(
        default=None,
        alias="status",
        description="Filter tasks by status.",
    ),
    priority: TaskPriority | None = Query(
        default=None,
        description="Filter tasks by priority.",
    ),
    assignee_id: int | None = Query(
        default=None,
        description="Filter tasks by assignee user ID.",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number.",
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of tasks per page.",
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
    summary="Create project task",
    description=(
        "Create a task in a project. "
        "Only ADMIN, workspace OWNER, or EDITOR "
        "can perform this action. The assignee must "
        "belong to the same workspace."
    ),
    responses=MUTATION_RESPONSES,
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
    summary="Get task details",
    description=(
        "Return task details when the authenticated user "
        "belongs to the task's workspace."
    ),
    responses=RESOURCE_RESPONSES,
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
    summary="Update task",
    description=(
        "Partially update task fields such as title, "
        "description, status, priority, due date, "
        "or assignee. Only ADMIN, workspace OWNER, "
        "or EDITOR can perform this action."
    ),
    responses=MUTATION_RESPONSES,
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
    summary="Delete task",
    description=(
        "Delete a task. Only ADMIN or workspace OWNER "
        "can perform this action."
    ),
    responses=RESOURCE_RESPONSES,
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