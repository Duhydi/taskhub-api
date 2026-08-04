from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserRegister
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.utils.security import hash_password, verify_password


class UserService:

    def __init__(
        self,
        repo: UserRepository,
    ):
        self.repo = repo

    async def register(
        self,
        data: UserRegister,
    ):
        existed = await self.repo.get_by_email(
            data.email
        )

        if existed:
            raise ValueError(
                "Email already exists"
            )

        user = User(
            username=data.username,
            email=data.email,
            password_hash=hash_password(
                data.password
            ),
        )

        return await self.repo.create(user)

    async def login(
        self,
        email: str,
        password: str,
    ) -> Token:

        print("=" * 50)
        print("Email nhập:", email)

        user = await self.repo.get_by_email(email)

        print("User:", user)

        if user:
            print("DB email:", user.email)
            print(
                "Verify:",
                verify_password(
                    password,
                    user.password_hash,
                ),
            )

        print("=" * 50)

        if user is None:
            raise ValueError(
                "Invalid email or password"
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password"
            )

        access_token = create_access_token(
            {"sub": user.email}
        )

        refresh_token = create_refresh_token(
            {"sub": user.email}
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

        payload = decode_token(refresh_token)

        if payload is None:
            raise ValueError("Invalid refresh token")

        email = payload.get("sub")

        if email is None:
            raise ValueError("Invalid refresh token")

        user = await self.repo.get_by_email(email)

        if user is None:
            raise ValueError("User not found")

        access_token = create_access_token(
            {
                "sub": user.email,
            }
        )

        new_refresh_token = create_refresh_token(
            {
                "sub": user.email,
            }
        )

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )