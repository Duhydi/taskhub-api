from typing import List

from fastapi import APIRouter, Depends

from app.dependencies.task import get_task_service
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    service=Depends(get_task_service),
):
    return service.get_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service=Depends(get_task_service),
):
    return service.get_task(task_id)


@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    service=Depends(get_task_service),
):
    return service.create_task(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task: TaskUpdate,
    service=Depends(get_task_service),
):
    return service.update_task(task_id, task)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    service=Depends(get_task_service),
):
    return service.delete_task(task_id)