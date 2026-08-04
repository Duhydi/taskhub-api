from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.dependencies.auth import get_current_user
from app.dependencies.label import get_label_service
from app.models.user import User
from app.schemas.label import (
    LabelCreate,
    LabelResponse,
    LabelUpdate,
)
from app.services.label_service import LabelService

router = APIRouter(
    tags=["Labels"],
)


@router.post(
    "/projects/{project_id}/labels",
    response_model=LabelResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_label(
    project_id: int,
    data: LabelCreate,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.create_label(
        project_id,
        data,
    )


@router.get(
    "/projects/{project_id}/labels",
    response_model=list[LabelResponse],
)
async def get_labels(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.get_labels(
        project_id
    )


@router.patch(
    "/labels/{label_id}",
    response_model=LabelResponse,
)
async def update_label(
    label_id: int,
    data: LabelUpdate,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.update_label(
        label_id,
        data,
    )


@router.delete(
    "/labels/{label_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_label(
    label_id: int,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    await service.delete_label(
        label_id
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )


@router.post(
    "/tasks/{task_id}/labels/{label_id}",
)
async def assign_label(
    task_id: int,
    label_id: int,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.assign_label(
        task_id,
        label_id,
    )


@router.delete(
    "/tasks/{task_id}/labels/{label_id}",
)
async def remove_label(
    task_id: int,
    label_id: int,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.remove_label(
        task_id,
        label_id,
    )