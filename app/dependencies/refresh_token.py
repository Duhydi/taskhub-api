from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)


def get_refresh_token_repo(
    db: AsyncSession = Depends(get_db),
):
    return RefreshTokenRepository(db)