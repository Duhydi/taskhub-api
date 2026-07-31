from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import UserRole

if TYPE_CHECKING:
    from app.models.workspace import Workspace
    from app.models.workspace_member import WorkspaceMember
    from app.models.task import Task
    from app.models.comment import Comment


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.USER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships

    owned_workspaces: Mapped[list["Workspace"]] = relationship(
        back_populates="owner",
    )

    workspace_memberships: Mapped[list["WorkspaceMember"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    created_tasks: Mapped[list["Task"]] = relationship(
        foreign_keys="Task.creator_id",
        back_populates="creator",
    )

    assigned_tasks: Mapped[list["Task"]] = relationship(
        foreign_keys="Task.assignee_id",
        back_populates="assignee",
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author",
    )