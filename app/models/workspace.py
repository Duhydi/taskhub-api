from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    owner = relationship(
        "User",
        back_populates="owned_workspaces",
    )
    members = relationship(
        "WorkspaceMember",
        back_populates="workspace",
        cascade="all, delete",
    )
    projects = relationship(
        "Project",
        back_populates="workspace",
        cascade="all, delete",
    )