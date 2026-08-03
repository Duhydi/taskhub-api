from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.user import UserRole


async def require_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only",
        )

    return current_user


async def require_member(
    current_user: User = Depends(get_current_user),
):
    return current_user