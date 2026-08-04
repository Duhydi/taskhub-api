from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.project import get_project_service
from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import ProjectService

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.get(
    "/",
    response_model=list[ProjectResponse],
)
async def get_projects(
    service: ProjectService = Depends(get_project_service),
):
    return await service.get_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    try:
        return await service.get_project(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
)
async def update_project(
    project_id: int,
    data: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    try:
        return await service.update_project(
            project_id,
            data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    try:
        await service.delete_project(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
@router.post(
    "/workspace/{workspace_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    workspace_id: int,
    data: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    return await service.create_project(
        workspace_id,
        data,
    )

@router.patch(
    "/{project_id}/archive",
    response_model=ProjectResponse,
)
async def archive_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    try:
        return await service.archive_project(
            project_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )