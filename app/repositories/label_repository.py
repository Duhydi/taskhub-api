from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.label import Label


class LabelRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        label: Label,
    ):
        self.db.add(label)

        await self.db.commit()
        await self.db.refresh(label)

        return label

    async def get_by_id(
        self,
        label_id: int,
    ):
        result = await self.db.execute(
            select(Label).where(
                Label.id == label_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_project(
        self,
        project_id: int,
    ):
        result = await self.db.execute(
            select(Label).where(
                Label.project_id == project_id
            )
        )

        return result.scalars().all()

    async def update(
        self,
        label: Label,
    ):
        await self.db.commit()
        await self.db.refresh(label)

        return label

    async def delete(
        self,
        label: Label,
    ):
        await self.db.delete(label)
        await self.db.commit()