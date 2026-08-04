from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.label_repository import (
    LabelRepository,
)
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.services.label_service import (
    LabelService,
)


def get_label_service(
    db: AsyncSession = Depends(get_db),
):
    return LabelService(
        label_repo=LabelRepository(db),
        project_repo=ProjectRepository(db),
        member_repo=WorkspaceMemberRepository(db),
        db=db,
    )