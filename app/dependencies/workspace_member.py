from fastapi import Depends

from app.db.dependencies import get_db
from app.repositories.user import UserRepository
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.services.workspace_member_service import (
    WorkspaceMemberService,
)


def get_workspace_member_service(
    db=Depends(get_db),
):
    return WorkspaceMemberService(
        workspace_repo=WorkspaceRepository(db),
        user_repo=UserRepository(db),
        member_repo=WorkspaceMemberRepository(db),
    )