from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.comment_repository import (
    CommentRepository,
)
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.services.comment_service import (
    CommentService,
)


def get_comment_service(
    db: AsyncSession = Depends(get_db),
):
    return CommentService(
        repo=CommentRepository(db),
        project_repo=ProjectRepository(db),
        member_repo=WorkspaceMemberRepository(db),
        db=db,
    )