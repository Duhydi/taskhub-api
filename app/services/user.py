from app.models.user import User
from app.repositories.user import UserRepository
from app.utils.security import (
    hash_password,
    verify_password,
)


class UserService:

    def __init__(
        self,
        repo: UserRepository,
    ):
        self.repo = repo

    async def get_me(
        self,
        current_user: User,
    ):
        return current_user

    async def update_profile(
        self,
        current_user: User,
        username: str,
    ):
        existed = await self.repo.get_by_username(
            username
        )

        if (
            existed
            and existed.id != current_user.id
        ):
            raise ValueError(
                "Username already exists"
            )

        current_user.username = username

        return await self.repo.update(
            current_user
        )

    async def change_password(
        self,
        current_user: User,
        old_password: str,
        new_password: str,
    ):

        if not verify_password(
            old_password,
            current_user.password_hash,
        ):
            raise ValueError(
                "Old password is incorrect",
            )

        current_user.password_hash = hash_password(
            new_password,
        )

        return await self.repo.update(
            current_user,
        )