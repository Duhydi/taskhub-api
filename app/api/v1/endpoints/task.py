from typing import List

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.dependencies.task import get_task_service
from app.models.user import User
from app.schemas.task import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.services.task_service import TaskService

router = APIRouter()


@router.get(
    "/",
    response_model=List[TaskResponse],
)
async def get_tasks(
    service: TaskService = Depends(get_task_service),
):
    return await service.get_tasks()


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
):
    return await service.get_task(task_id)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(
        task,
        current_user,
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    return await service.update_task(
        task_id,
        task,
        current_user,
    )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    await service.delete_task(
        task_id,
        current_user,
    )