from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


class ProjectRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def create(
        self,
        project: Project,
    ):
        self.db.add(project)

        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def get_by_id(
        self,
        project_id: int,
    ):
        result = await self.db.execute(
            select(Project).where(
                Project.id == project_id
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(Project)
        )

        return result.scalars().all()

    async def update(
        self,
        project: Project,
    ):
        await self.db.commit()
        await self.db.refresh(project)

        return project

    async def delete(
        self,
        project: Project,
    ):
        await self.db.delete(project)
        await self.db.commit()

    async def get_by_workspace(
        self,
        workspace_id: int,
    ):
        result = await self.db.execute(
            select(Project)
            .where(
                Project.workspace_id == workspace_id
            )
            .order_by(Project.created_at.desc())
        )

        return result.scalars().all()
    
    async def get_workspace_id(
        self,
        project_id: int,
    ):
        project = await self.get_by_id(
            project_id
        )

        if project is None:
            return None

        return project.workspace_id