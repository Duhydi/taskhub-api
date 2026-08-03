from fastapi import APIRouter, Depends

from app.dependencies.auth import (
    get_current_user,
    require_role,
)

from app.models.user import User, UserRole
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/admin")
async def admin_only(
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    return {
        "message": "Welcome Admin",
        "user": current_user.username,
    }

from app.exceptions.handlers import AppException
from fastapi import status


@router.get("/test-error")
async def test_error():
    raise AppException(
        "Something went wrong",
        status.HTTP_400_BAD_REQUEST,
    )