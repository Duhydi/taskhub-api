from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        refresh_token: RefreshToken,
    ):
        self.db.add(refresh_token)

        await self.db.commit()
        await self.db.refresh(refresh_token)

        return refresh_token

    async def get_by_token(
        self,
        token: str,
    ):
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token == token
            )
        )

        return result.scalar_one_or_none()

    async def revoke(
        self,
        refresh_token: RefreshToken,
    ):
        refresh_token.revoked = True

        await self.db.commit()