from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user
from app.dependencies.workspace_member import (
    get_workspace_member_service,
)
from app.models.user import User
from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)
from app.services.workspace_member_service import (
    WorkspaceMemberService,
)


def require_workspace_roles(
    *allowed_roles: WorkspaceMemberRole,
):
    async def checker(
        workspace_id: int,
        current_user: User = Depends(get_current_user),
        service: WorkspaceMemberService = Depends(
            get_workspace_member_service
        ),
    ):
        member = await service.member_repo.get_member(
            workspace_id=workspace_id,
            user_id=current_user.id,
        )

        if member is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a workspace member",
            )

        if member.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return checker