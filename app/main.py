from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.task import router as task_router
from app.core.config import settings
from app.api.v1.endpoints.user import router as user_router
from app.middlewares.logging import logging_middleware
from app.exceptions.handlers import (
    AppException,
    app_exception_handler,
)
from app.api.v1.endpoints.workspace import (
    router as workspace_router,
)
from app.api.v1.endpoints.workspace_member import (
    router as workspace_member_router,
)
from app.api.v1.endpoints.project import (
    router as project_router,
)
from app.api.v1.endpoints.label import (
    router as label_router,
)
from app.api.v1.endpoints.comment import (
    router as comment_router,
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting TaskHub API...")
    yield
    print("Stopping TaskHub API...")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "TaskHub is a task management API supporting "
        "users, workspaces, projects, tasks, labels, "
        "comments, JWT authentication, RBAC, pagination, "
        "and Redis caching."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.middleware("http")(logging_middleware)

@app.get("/")
def root():
    return {"message": "TaskHub API"}


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    task_router,
    prefix="/api/v1",
)
app.include_router(
    user_router,
    prefix="/api/v1",
)
app.add_exception_handler(
    AppException,
    app_exception_handler,
)
app.include_router(
    workspace_router,
    prefix="/api/v1",
)
app.include_router(
    workspace_member_router,
    prefix="/api/v1",
)
app.include_router(
    project_router,
    prefix="/api/v1",
)
app.include_router(
    label_router,
    prefix="/api/v1",
)
app.include_router(
    comment_router,
    prefix="/api/v1",
)