from app.models.project import Project
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
)
from app.repositories.project_repository import (
    ProjectRepository,
)

from app.models.project import ProjectStatus
class ProjectService:

    def __init__(
        self,
        repo: ProjectRepository,
    ):
        self.repo = repo

    async def create_project(
        self,
        workspace_id: int,
        data: ProjectCreate,
    ):
        project = Project(
            workspace_id=workspace_id,
            name=data.name,
            description=data.description,
        )

        return await self.repo.create(project)

    async def get_projects(self):
        return await self.repo.get_all()

    async def get_project(
        self,
        project_id: int,
    ):
        project = await self.repo.get_by_id(project_id)

        if project is None:
            raise ValueError("Project not found")

        return project

    async def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
    ):
        project = await self.repo.get_by_id(project_id)

        if project is None:
            raise ValueError("Project not found")

        if data.name is not None:
            project.name = data.name

        if data.description is not None:
            project.description = data.description

        return await self.repo.update(project)

    async def delete_project(
        self,
        project_id: int,
    ):
        project = await self.repo.get_by_id(project_id)

        if project is None:
            raise ValueError("Project not found")

        await self.repo.delete(project)
    
    async def archive_project(
        self,
        project_id: int,
    ):
        project = await self.repo.get_by_id(
            project_id
        )

        if project is None:
            raise ValueError("Project not found")

        project.status = ProjectStatus.ARCHIVED

        return await self.repo.update(project)