from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.core.api_responses import (
    MUTATION_RESPONSES,
    RESOURCE_RESPONSES,
)
from app.dependencies.auth import get_current_user
from app.dependencies.user import get_user_service
from app.models.user import User
from app.schemas.user import (
    ChangePasswordRequest,
    UserResponse,
    UserUpdate,
)
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description=(
        "Return the profile of the authenticated user."
    ),
    responses=RESOURCE_RESPONSES,
)
async def get_me(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return await service.get_me(
        current_user=current_user,
    )


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description=(
        "Partially update the authenticated user's profile."
    ),
    responses=MUTATION_RESPONSES,
)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.update_profile(
            current_user=current_user,
            username=data.username,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.patch(
    "/change-password",
    summary="Change current user password",
    description=(
        "Change the authenticated user's password after "
        "verifying the current password."
    ),
    responses=MUTATION_RESPONSES,
)
async def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    try:
        await service.change_password(
            current_user=current_user,
            old_password=data.old_password,
            new_password=data.new_password,
        )

        return {
            "message": "Password changed successfully",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc