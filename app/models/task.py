from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.task_enum import (
    TaskPriority,
    TaskStatus,
)
from app.models.label import Label
if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
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

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="tasks",
    )

    owner: Mapped["User"] = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_tasks",
    )

    assignee: Mapped["User | None"] = relationship(
        "User",
        foreign_keys=[assignee_id],
        back_populates="assigned_tasks",
    )
    labels: Mapped[list["Label"]] = relationship(
        "Label",
        secondary="task_labels",
        back_populates="tasks",
    )