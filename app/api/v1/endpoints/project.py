from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.core.api_responses import (
    MUTATION_RESPONSES,
    RESOURCE_RESPONSES,
)
from app.dependencies.auth import get_current_user
from app.dependencies.project import get_project_service
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import ProjectService

router = APIRouter(
    tags=["Projects"],
)


@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create workspace project",
    description=(
        "Create a project in a workspace. "
        "Only ADMIN, OWNER, or EDITOR can perform this action."
    ),
    responses=MUTATION_RESPONSES,
)
async def create_project(
    workspace_id: int,
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(
        get_project_service
    ),
):
    return await service.create_project(
        workspace_id=workspace_id,
        data=data,
        current_user=current_user,
    )


@router.get(
    "/workspaces/{workspace_id}/projects",
    response_model=list[ProjectResponse],
    summary="List workspace projects",
    description=(
        "Return all projects in a workspace. "
        "The authenticated user must belong to the workspace."
    ),
    responses=RESOURCE_RESPONSES,
)
async def get_projects(
    workspace_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(
        get_project_service
    ),
):
    return await service.get_projects(
        workspace_id=workspace_id,
        current_user=current_user,
    )


@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Get project details",
    description=(
        "Return project details when the authenticated user "
        "has access to the project's workspace."
    ),
    responses=RESOURCE_RESPONSES,
)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(
        get_project_service
    ),
):
    return await service.get_project(
        project_id=project_id,
        current_user=current_user,
    )


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
    description=(
        "Update a project. "
        "Only ADMIN, OWNER, or EDITOR can perform this action."
    ),
    responses=MUTATION_RESPONSES,
)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(
        get_project_service
    ),
):
    return await service.update_project(
        project_id=project_id,
        data=data,
        current_user=current_user,
    )


@router.patch(
    "/projects/{project_id}/archive",
    response_model=ProjectResponse,
    summary="Archive project",
    description=(
        "Archive an active project. "
        "Only ADMIN or workspace OWNER can perform this action."
    ),
    responses=MUTATION_RESPONSES,
)
async def archive_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(
        get_project_service
    ),
):
    return await service.archive_project(
        project_id=project_id,
        current_user=current_user,
    )


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project",
    description=(
        "Delete a project. "
        "Only ADMIN or workspace OWNER can perform this action."
    ),
    responses=RESOURCE_RESPONSES,
)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: ProjectService = Depends(
        get_project_service
    ),
):
    await service.delete_project(
        project_id=project_id,
        current_user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )