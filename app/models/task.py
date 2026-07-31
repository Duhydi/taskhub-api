from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import TaskPriority, TaskStatus

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User
    from app.models.comment import Comment
    from app.models.task_label import TaskLabel


class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus),
        default=TaskStatus.TODO,
        nullable=False,
    )

    priority: Mapped[TaskPriority] = mapped_column(
        SqlEnum(TaskPriority),
        default=TaskPriority.MEDIUM,
        nullable=False,
    )

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    project: Mapped["Project"] = relationship(
        back_populates="tasks",
    )

    creator: Mapped["User"] = relationship(
        foreign_keys=[creator_id],
        back_populates="created_tasks",
    )

    assignee: Mapped["User | None"] = relationship(
        foreign_keys=[assignee_id],
        back_populates="assigned_tasks",
    )

    comments: Mapped[list["Comment"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
    )

    task_labels: Mapped[list["TaskLabel"]] = relationship(
        back_populates="task",
        cascade="all, delete-orphan",
    )