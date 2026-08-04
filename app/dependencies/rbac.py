from fastapi import HTTPException, status

from app.models.user import User, UserRole
from app.models.workspace_member import WorkspaceMember
from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)


def require_workspace_role(
    member: WorkspaceMember | None,
    *allowed_roles: WorkspaceMemberRole,
) -> None:
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


def require_admin(
    current_user: User,
) -> None:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin only",
        )