from fastapi import Depends

from app.db.dependencies import get_db
from app.repositories.user import UserRepository
from app.services.user import UserService


def get_user_service(
    db=Depends(get_db),
):
    return UserService(
        UserRepository(db),
    )