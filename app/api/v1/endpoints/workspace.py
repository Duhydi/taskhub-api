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
from app.dependencies.auth import get_current_user
from app.dependencies.workspace import (
    get_workspace_service,
)
from app.models.user import User
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceUpdate,
)
from app.services.workspace_service import (
    WorkspaceService,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create workspace",
    description=(
        "Create a new workspace. The authenticated user "
        "becomes the workspace OWNER."
    ),
    responses=MUTATION_RESPONSES,
)
async def create_workspace(
    data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return await service.create(
        data=data,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[WorkspaceResponse],
    summary="List workspaces",
    description=(
        "Return the available workspaces for the "
        "authenticated user."
    ),
    responses=RESOURCE_RESPONSES,
)
async def get_workspaces(
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return await service.get_all()


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
    summary="Get workspace details",
    description=(
        "Return details of the requested workspace."
    ),
    responses=RESOURCE_RESPONSES,
)
async def get_workspace(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    try:
        return await service.get_by_id(
            workspace_id=workspace_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
    summary="Update workspace",
    description=(
        "Update the workspace name. Only the workspace "
        "OWNER or an ADMIN can perform this action."
    ),
    responses=MUTATION_RESPONSES,
)
async def update_workspace(
    workspace_id: int,
    data: WorkspaceUpdate,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    try:
        return await service.update(
            workspace_id=workspace_id,
            data=data,
            current_user=current_user,
        )

    except ValueError as exc:
        error_message = str(exc)

        if error_message == "Workspace not found":
            error_status = status.HTTP_404_NOT_FOUND
        else:
            error_status = status.HTTP_403_FORBIDDEN

        raise HTTPException(
            status_code=error_status,
            detail=error_message,
        ) from exc


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete workspace",
    description=(
        "Delete a workspace and its related resources. "
        "Only the workspace OWNER or an ADMIN can perform "
        "this action."
    ),
    responses=RESOURCE_RESPONSES,
)
async def delete_workspace(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    try:
        await service.delete(
            workspace_id=workspace_id,
            current_user=current_user,
        )

    except ValueError as exc:
        error_message = str(exc)

        if error_message == "Workspace not found":
            error_status = status.HTTP_404_NOT_FOUND
        else:
            error_status = status.HTTP_403_FORBIDDEN

        raise HTTPException(
            status_code=error_status,
            detail=error_message,
        ) from exc

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )