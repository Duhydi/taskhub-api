from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.workspace_member import (
    get_workspace_member_service,
)
from app.schemas.workspace_member import (
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
)
from app.services.workspace_member_service import (
    WorkspaceMemberService,
)
from app.dependencies.workspace_rbac import (
    require_workspace_roles,
)
from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)
from app.models.user import User

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace Members"],
)


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def invite_member(
    workspace_id: int,
    data: WorkspaceMemberCreate,
    current_user: User = Depends(
        require_workspace_roles(
            WorkspaceMemberRole.OWNER,
        )
    ),
    service: WorkspaceMemberService = Depends(
        get_workspace_member_service
    ),
):
    try:
        return await service.invite_member(
            workspace_id,
            data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.get(
    "/{workspace_id}/members",
    response_model=list[WorkspaceMemberResponse],
)
async def get_members(
    workspace_id: int,
    service: WorkspaceMemberService = Depends(
        get_workspace_member_service
    ),
):
    return await service.get_members(
        workspace_id
    )


@router.delete(
    "/{workspace_id}/members/{user_id}",
)
async def remove_member(
    workspace_id: int,
    user_id: int,
    current_user: User = Depends(
        require_workspace_roles(
            WorkspaceMemberRole.OWNER,
        )
    ),
    service: WorkspaceMemberService = Depends(
        get_workspace_member_service
    ),
):
    try:
        await service.remove_member(
            workspace_id,
            user_id,
        )

        return {
            "message": "Member removed successfully",
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )