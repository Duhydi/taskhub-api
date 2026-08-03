from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserRegister
from app.utils.jwt import create_access_token
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

        user = await self.repo.get_by_email(
            email
        )

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
            {
                "sub": user.email,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )