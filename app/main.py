from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.task import router as task_router
from app.core.config import settings
from app.api.v1.endpoints.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting TaskHub API...")
    yield
    print("Stopping TaskHub API...")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "TaskHub API"}


app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    task_router,
    prefix="/api/v1/tasks",
)

app.include_router(
    user_router,
    prefix="/api/v1",
)