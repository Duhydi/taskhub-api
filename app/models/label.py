from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.task_label import TaskLabel


class Label(Base):
    __tablename__ = "labels"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    color: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    task_labels: Mapped[list["TaskLabel"]] = relationship(
        back_populates="label",
        cascade="all, delete-orphan",
    )