from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from app.core.api_responses import (
    MUTATION_RESPONSES,
    RESOURCE_RESPONSES,
)
from app.dependencies.workspace_member import (
    get_workspace_member_service,
)
from app.dependencies.workspace_rbac import (
    require_workspace_roles,
)
from app.models.user import User
from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)
from app.schemas.workspace_member import (
    WorkspaceMemberCreate,
    WorkspaceMemberResponse,
)
from app.services.workspace_member_service import (
    WorkspaceMemberService,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace Members"],
)


@router.post(
    "/{workspace_id}/members",
    response_model=WorkspaceMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Invite workspace member",
    description=(
        "Add a user to a workspace with a specified role. "
        "Only the workspace OWNER can perform this action."
    ),
    responses=MUTATION_RESPONSES,
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
            workspace_id=workspace_id,
            data=data,
        )

    except ValueError as exc:
        error_message = str(exc)

        if error_message in {
            "Workspace not found",
            "User not found",
        }:
            error_status = status.HTTP_404_NOT_FOUND
        elif error_message == "User already in workspace":
            error_status = status.HTTP_409_CONFLICT
        else:
            error_status = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=error_status,
            detail=error_message,
        ) from exc


@router.get(
    "/{workspace_id}/members",
    response_model=list[WorkspaceMemberResponse],
    summary="List workspace members",
    description=(
        "Return all members of a workspace. "
        "The authenticated user must belong to the workspace."
    ),
    responses=RESOURCE_RESPONSES,
)
async def get_members(
    workspace_id: int,
    current_user: User = Depends(
        require_workspace_roles(
            WorkspaceMemberRole.OWNER,
            WorkspaceMemberRole.EDITOR,
            WorkspaceMemberRole.VIEWER,
        )
    ),
    service: WorkspaceMemberService = Depends(
        get_workspace_member_service
    ),
):
    return await service.get_members(
        workspace_id=workspace_id,
    )


@router.delete(
    "/{workspace_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove workspace member",
    description=(
        "Remove a member from a workspace. "
        "Only the workspace OWNER can perform this action. "
        "The workspace OWNER cannot be removed."
    ),
    responses=RESOURCE_RESPONSES,
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
            workspace_id=workspace_id,
            user_id=user_id,
        )

    except ValueError as exc:
        error_message = str(exc)

        if error_message == "Member not found":
            error_status = status.HTTP_404_NOT_FOUND
        elif error_message == "Workspace owner cannot be removed":
            error_status = status.HTTP_400_BAD_REQUEST
        else:
            error_status = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=error_status,
            detail=error_message,
        ) from exc

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )