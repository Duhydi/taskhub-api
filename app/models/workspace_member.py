from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import WorkspaceRole

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.workspace import Workspace


class WorkspaceMember(Base, TimestampMixin):
    __tablename__ = "workspace_members"

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role: Mapped[WorkspaceRole] = mapped_column(
        SqlEnum(WorkspaceRole),
        default=WorkspaceRole.VIEWER,
        nullable=False,
    )

    workspace: Mapped["Workspace"] = relationship(
        back_populates="members",
    )

    user: Mapped["User"] = relationship(
        back_populates="workspace_memberships",
    )