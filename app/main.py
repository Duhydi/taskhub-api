from app.api.v1.endpoints.task import router as task_router

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings


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
    task_router,
    prefix="/tasks",
    tags=["Tasks"]
)