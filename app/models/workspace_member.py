from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.workspace_member_enum import WorkspaceMemberRole


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    __table_args__ = (
        UniqueConstraint(
            "workspace_id",
            "user_id",
            name="uq_workspace_member",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    role: Mapped[WorkspaceMemberRole] = mapped_column(
        SqlEnum(WorkspaceMemberRole),
        default=WorkspaceMemberRole.VIEWER,
        nullable=False,
    )

    workspace = relationship(
        "Workspace",
        back_populates="members",
    )

    user = relationship(
        "User",
        back_populates="workspace_members",
    )