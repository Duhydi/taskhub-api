from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.services.workspace_service import (
    WorkspaceService,
)


def get_workspace_service(
    db: AsyncSession = Depends(get_db),
):
    workspace_repo = WorkspaceRepository(db)
    member_repo = WorkspaceMemberRepository(db)

    return WorkspaceService(
        repo=workspace_repo,
        member_repo=member_repo,
    )