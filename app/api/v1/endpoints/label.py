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
    summary="Create project label",
    description=(
        "Create a label in a project. "
        "Only ADMIN, workspace OWNER, or EDITOR "
        "can perform this action."
    ),
    responses=MUTATION_RESPONSES,
)
async def create_label(
    project_id: int,
    data: LabelCreate,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.create_label(
        project_id=project_id,
        data=data,
        current_user=current_user,
    )


@router.get(
    "/projects/{project_id}/labels",
    response_model=list[LabelResponse],
    summary="List project labels",
    description=(
        "Return all labels belonging to a project. "
        "The authenticated user must have access "
        "to the project's workspace."
    ),
    responses=RESOURCE_RESPONSES,
)
async def get_labels(
    project_id: int,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.get_labels(
        project_id=project_id,
        current_user=current_user,
    )


@router.patch(
    "/labels/{label_id}",
    response_model=LabelResponse,
    summary="Update label",
    description=(
        "Partially update a label name or color. "
        "Only ADMIN, workspace OWNER, or EDITOR "
        "can perform this action."
    ),
    responses=MUTATION_RESPONSES,
)
async def update_label(
    label_id: int,
    data: LabelUpdate,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.update_label(
        label_id=label_id,
        data=data,
        current_user=current_user,
    )


@router.delete(
    "/labels/{label_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete label",
    description=(
        "Delete a label from its project. "
        "Only ADMIN, workspace OWNER, or EDITOR "
        "can perform this action."
    ),
    responses=RESOURCE_RESPONSES,
)
async def delete_label(
    label_id: int,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    await service.delete_label(
        label_id=label_id,
        current_user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )


@router.post(
    "/tasks/{task_id}/labels/{label_id}",
    summary="Assign label to task",
    description=(
        "Assign a label to a task. "
        "The task and label must belong to the same project. "
        "Only ADMIN, workspace OWNER, or EDITOR "
        "can perform this action."
    ),
    responses=MUTATION_RESPONSES,
)
async def assign_label(
    task_id: int,
    label_id: int,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.assign_label(
        task_id=task_id,
        label_id=label_id,
        current_user=current_user,
    )


@router.delete(
    "/tasks/{task_id}/labels/{label_id}",
    summary="Remove label from task",
    description=(
        "Remove a label from a task. "
        "Only ADMIN, workspace OWNER, or EDITOR "
        "can perform this action."
    ),
    responses=MUTATION_RESPONSES,
)
async def remove_label(
    task_id: int,
    label_id: int,
    current_user: User = Depends(get_current_user),
    service: LabelService = Depends(get_label_service),
):
    return await service.remove_label(
        task_id=task_id,
        label_id=label_id,
        current_user=current_user,
    )