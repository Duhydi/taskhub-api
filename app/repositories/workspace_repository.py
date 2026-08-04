from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workspace import Workspace


class WorkspaceRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        workspace: Workspace,
    ):
        self.db.add(workspace)

        await self.db.commit()
        await self.db.refresh(workspace)

        return workspace

    async def get_by_id(
        self,
        workspace_id: int,
    ):
        result = await self.db.execute(
            select(Workspace).where(
                Workspace.id == workspace_id
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(Workspace)
        )

        return result.scalars().all()

    async def update(
        self,
        workspace: Workspace,
    ):
        await self.db.commit()
        await self.db.refresh(workspace)

        return workspace

    async def delete(
        self,
        workspace: Workspace,
    ):
        await self.db.delete(workspace)
        await self.db.commit()