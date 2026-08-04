from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.services.project_service import (
    ProjectService,
)


def get_project_service(
    db: AsyncSession = Depends(get_db),
):
    return ProjectService(
        repo=ProjectRepository(db),
        workspace_repo=WorkspaceRepository(db),
        member_repo=WorkspaceMemberRepository(db),
    )