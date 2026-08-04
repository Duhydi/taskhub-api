from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.task import Task


class Label(Base):
    __tablename__ = "labels"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "name",
            name="uq_label_project_name",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="labels",
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_labels",
        back_populates="labels",
    )