from fastapi import Depends

from app.db.dependencies import get_db
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.services.project_service import (
    ProjectService,
)


def get_project_service(
    db=Depends(get_db),
):
    repo = ProjectRepository(db)

    return ProjectService(repo)