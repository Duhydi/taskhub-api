from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workspace_member import WorkspaceMember


class WorkspaceMemberRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        member: WorkspaceMember,
    ):
        self.db.add(member)

        await self.db.commit()
        await self.db.refresh(member)

        return member

    async def get_member(
        self,
        workspace_id: int,
        user_id: int,
    ):
        result = await self.db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_members(
        self,
        workspace_id: int,
    ):
        result = await self.db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id
            )
        )

        return result.scalars().all()

    async def delete(
        self,
        member: WorkspaceMember,
    ):
        await self.db.delete(member)
        await self.db.commit()