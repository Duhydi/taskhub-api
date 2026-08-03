from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)