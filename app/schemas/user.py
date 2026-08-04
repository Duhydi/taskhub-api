from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    username: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

from pydantic import BaseModel, Field


class UserUpdate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )


class ChangePassword(BaseModel):
    old_password: str

    new_password: str = Field(
        min_length=6,
        max_length=100,
    )