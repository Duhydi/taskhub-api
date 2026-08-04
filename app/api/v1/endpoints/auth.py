from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.auth_service import (
    get_auth_service,
)
from app.schemas.auth import (
    Token,
    RefreshTokenRequest,
    LogoutRequest,
)
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import (
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: UserRegister,
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.register(data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.login(
            email=form_data.username,
            password=form_data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    
@router.post(
    "/refresh",
    response_model=Token,
)
async def refresh_token(
    data: RefreshTokenRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.refresh_access_token(
            data.refresh_token,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

@router.post("/logout")
async def logout(
    data: LogoutRequest,
    service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.logout(
            data.refresh_token
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )