from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment


class CommentRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        comment: Comment,
    ):
        self.db.add(comment)

        await self.db.commit()
        await self.db.refresh(comment)

        return comment

    async def get_by_id(
        self,
        comment_id: int,
    ):
        result = await self.db.execute(
            select(Comment).where(
                Comment.id == comment_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_task(
        self,
        task_id: int,
    ):
        result = await self.db.execute(
            select(Comment)
            .where(
                Comment.task_id == task_id
            )
            .order_by(
                Comment.created_at.asc()
            )
        )

        return result.scalars().all()

    async def update(
        self,
        comment: Comment,
    ):
        await self.db.commit()

        await self.db.refresh(comment)

        return comment

    async def delete(
        self,
        comment: Comment,
    ):
        await self.db.delete(comment)

        await self.db.commit()