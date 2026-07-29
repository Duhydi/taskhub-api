from app.repositories import task_repository
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks():
    return task_repository.get_all()


def get_task(task_id: int):
    return task_repository.get_by_id(task_id)


def create_task(task: TaskCreate):
    new_task = {
        "id": len(task_repository.get_all()) + 1,
        "title": task.title,
        "description": task.description,
    }

    return task_repository.create(new_task)


def update_task(task_id: int, task: TaskUpdate):
    data = {
        "title": task.title,
        "description": task.description,
    }

    return task_repository.update(task_id, data)


def delete_task(task_id: int):
    return task_repository.delete(task_id)