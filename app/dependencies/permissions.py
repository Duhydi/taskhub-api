from fastapi import HTTPException, status

from app.models.task import Task
from app.models.user import User, UserRole


def check_task_permission(
    user: User,
    task: Task,
):
    if user.role == UserRole.ADMIN:
        return

    if task.created_by == user.id:
        return

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Permission denied",
    )