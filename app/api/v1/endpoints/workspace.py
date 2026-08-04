from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.dependencies.auth import get_current_user
from app.dependencies.workspace import (
    get_workspace_service,
)
from app.models.user import User
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate,
    WorkspaceResponse,
)
from app.services.workspace_service import (
    WorkspaceService,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspace"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_workspace(
    data: WorkspaceCreate,
    current_user: User = Depends(get_current_user),
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return await service.create(
        data,
        current_user,
    )


@router.get(
    "",
    response_model=list[WorkspaceResponse],
)
async def get_workspaces(
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    return await service.get_all()


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
)
async def get_workspace(
    workspace_id: int,
    service: WorkspaceService = Depends(
        get_workspace_service
    ),
):
    try:
        return await service.get_by_id(
            workspace_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
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
            workspace_id,
            data,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
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
            workspace_id,
            current_user,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )