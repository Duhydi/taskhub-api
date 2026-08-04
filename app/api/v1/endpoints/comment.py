from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from app.dependencies.auth import get_current_user
from app.dependencies.comment import (
    get_comment_service,
)
from app.models.user import User
from app.schemas.comment import (
    CommentCreate,
    CommentResponse,
    CommentUpdate,
)
from app.services.comment_service import (
    CommentService,
)

router = APIRouter(
    tags=["Comments"],
)


@router.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    task_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(
        get_comment_service
    ),
):
    return await service.create_comment(
        task_id=task_id,
        data=data,
        current_user=current_user,
    )


@router.get(
    "/tasks/{task_id}/comments",
    response_model=list[CommentResponse],
)
async def get_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(
        get_comment_service
    ),
):
    return await service.get_comments(
        task_id=task_id,
        current_user=current_user,
    )


@router.patch(
    "/comments/{comment_id}",
    response_model=CommentResponse,
)
async def update_comment(
    comment_id: int,
    data: CommentUpdate,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(
        get_comment_service
    ),
):
    return await service.update_comment(
        comment_id=comment_id,
        data=data,
        current_user=current_user,
    )


@router.delete(
    "/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    service: CommentService = Depends(
        get_comment_service
    ),
):
    await service.delete_comment(
        comment_id=comment_id,
        current_user=current_user,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )