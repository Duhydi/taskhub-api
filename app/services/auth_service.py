from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserRegister
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.utils.security import (
    hash_password,
    verify_password,
)


class AuthService:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.user_repo = UserRepository(db)
        self.refresh_repo = RefreshTokenRepository(db)

    async def register(
        self,
        data: UserRegister,
    ):
        existed = await self.user_repo.get_by_email(
            data.email,
        )

        if existed:
            raise ValueError("Email already exists")

        user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(
                data.password,
            ),
        )

        return await self.user_repo.create(user)

    async def login(
        self,
        email: str,
        password: str,
    ) -> Token:

        user = await self.user_repo.get_by_email(
            email,
        )

        if user is None:
            raise ValueError(
                "Invalid email or password",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password",
            )

        access_token = create_access_token(
            {
                "sub": user.email,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": user.email,
            }
        )

        await self.refresh_repo.create(
            RefreshToken(
                token=refresh_token,
                user_id=user.id,
            )
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh_access_token(
        self,
        refresh_token: str,
    ) -> Token:

        payload = decode_token(
            refresh_token,
        )

        if payload is None:
            raise ValueError(
                "Invalid refresh token",
            )

        db_token = await self.refresh_repo.get_by_token(
            refresh_token,
        )

        if db_token is None:
            raise ValueError(
                "Refresh token not found",
            )

        if db_token.revoked:
            raise ValueError(
                "Refresh token revoked",
            )

        email = payload.get("sub")

        if email is None:
            raise ValueError(
                "Invalid refresh token",
            )

        user = await self.user_repo.get_by_email(
            email,
        )

        if user is None:
            raise ValueError(
                "User not found",
            )

        access_token = create_access_token(
            {
                "sub": user.email,
            }
        )

        new_refresh = create_refresh_token(
            {
                "sub": user.email,
            }
        )

        await self.refresh_repo.create(
            RefreshToken(
                token=new_refresh,
                user_id=user.id,
            )
        )

        await self.refresh_repo.revoke(
            db_token,
        )

        return Token(
            access_token=access_token,
            refresh_token=new_refresh,
            token_type="bearer",
        )

    async def logout(
        self,
        refresh_token: str,
    ):

        db_token = await self.refresh_repo.get_by_token(
            refresh_token,
        )

        if db_token is None:
            raise ValueError(
                "Refresh token not found",
            )

        if db_token.revoked:
            raise ValueError(
                "Refresh token already revoked",
            )

        await self.refresh_repo.revoke(
            db_token,
        )

        return {
            "message": "Logout successful",
        }