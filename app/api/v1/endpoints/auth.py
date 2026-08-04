from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from app.core.api_responses import (
    BAD_REQUEST_RESPONSE,
    UNAUTHORIZED_RESPONSE,
)
from app.dependencies.auth_service import (
    get_auth_service,
)
from app.schemas.auth import (
    LogoutRequest,
    RefreshTokenRequest,
    Token,
)
from app.schemas.user import (
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
    summary="Register new user",
    description=(
        "Create a new TaskHub account using username, "
        "email, and password."
    ),
    responses=BAD_REQUEST_RESPONSE,
)
async def register(
    data: UserRegister,
    service: AuthService = Depends(
        get_auth_service
    ),
):
    try:
        return await service.register(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(
    "/login",
    response_model=Token,
    summary="Login and obtain JWT tokens",
    description=(
        "Authenticate using email in the username field "
        "and password. Returns an access token and "
        "a refresh token."
    ),
    responses=UNAUTHORIZED_RESPONSE,
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(
        get_auth_service
    ),
):
    try:
        return await service.login(
            email=form_data.username,
            password=form_data.password,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh JWT tokens",
    description=(
        "Validate an active refresh token and issue "
        "a new access token and refresh token."
    ),
    responses=UNAUTHORIZED_RESPONSE,
)
async def refresh_token(
    data: RefreshTokenRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):
    try:
        return await service.refresh_access_token(
            data.refresh_token
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={
                "WWW-Authenticate": "Bearer",
            },
        ) from exc


@router.post(
    "/logout",
    summary="Logout and revoke refresh token",
    description=(
        "Revoke the submitted refresh token so it "
        "cannot be used again."
    ),
    responses={
        **BAD_REQUEST_RESPONSE,
        **UNAUTHORIZED_RESPONSE,
    },
)
async def logout(
    data: LogoutRequest,
    service: AuthService = Depends(
        get_auth_service
    ),
):
    try:
        return await service.logout(
            data.refresh_token
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc