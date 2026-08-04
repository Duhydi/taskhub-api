from fastapi import HTTPException, status

from app.dependencies.rbac import require_workspace_role
from app.models.project import Project, ProjectStatus
from app.models.user import User, UserRole
from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate,
)


class ProjectService:

    def __init__(
        self,
        repo: ProjectRepository,
        workspace_repo: WorkspaceRepository,
        member_repo: WorkspaceMemberRepository,
    ):
        self.repo = repo
        self.workspace_repo = workspace_repo
        self.member_repo = member_repo

    async def create_project(
        self,
        workspace_id: int,
        data: ProjectCreate,
        current_user: User,
    ):
        await self._get_workspace_or_404(
            workspace_id
        )

        await self._require_roles(
            workspace_id=workspace_id,
            current_user=current_user,
            allowed_roles=(
                WorkspaceMemberRole.OWNER,
                WorkspaceMemberRole.EDITOR,
            ),
        )

        project = Project(
            workspace_id=workspace_id,
            name=data.name,
            description=data.description,
        )

        return await self.repo.create(project)

    async def get_projects(
        self,
        workspace_id: int,
        current_user: User,
    ):
        await self._get_workspace_or_404(
            workspace_id
        )

        await self._require_roles(
            workspace_id=workspace_id,
            current_user=current_user,
            allowed_roles=(
                WorkspaceMemberRole.OWNER,
                WorkspaceMemberRole.EDITOR,
                WorkspaceMemberRole.VIEWER,
            ),
        )

        return await self.repo.get_by_workspace(
            workspace_id
        )

    async def get_project(
        self,
        project_id: int,
        current_user: User,
    ):
        project = await self._get_project_or_404(
            project_id
        )

        await self._require_roles(
            workspace_id=project.workspace_id,
            current_user=current_user,
            allowed_roles=(
                WorkspaceMemberRole.OWNER,
                WorkspaceMemberRole.EDITOR,
                WorkspaceMemberRole.VIEWER,
            ),
        )

        return project

    async def update_project(
        self,
        project_id: int,
        data: ProjectUpdate,
        current_user: User,
    ):
        project = await self._get_project_or_404(
            project_id
        )

        await self._require_roles(
            workspace_id=project.workspace_id,
            current_user=current_user,
            allowed_roles=(
                WorkspaceMemberRole.OWNER,
                WorkspaceMemberRole.EDITOR,
            ),
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(project, field, value)

        return await self.repo.update(project)

    async def archive_project(
        self,
        project_id: int,
        current_user: User,
    ):
        project = await self._get_project_or_404(
            project_id
        )

        await self._require_roles(
            workspace_id=project.workspace_id,
            current_user=current_user,
            allowed_roles=(
                WorkspaceMemberRole.OWNER,
            ),
        )

        project.status = ProjectStatus.ARCHIVED

        return await self.repo.update(project)

    async def delete_project(
        self,
        project_id: int,
        current_user: User,
    ) -> None:
        project = await self._get_project_or_404(
            project_id
        )

        await self._require_roles(
            workspace_id=project.workspace_id,
            current_user=current_user,
            allowed_roles=(
                WorkspaceMemberRole.OWNER,
            ),
        )

        await self.repo.delete(project)

    async def _get_project_or_404(
        self,
        project_id: int,
    ):
        project = await self.repo.get_by_id(
            project_id
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project

    async def _get_workspace_or_404(
        self,
        workspace_id: int,
    ):
        workspace = await self.workspace_repo.get_by_id(
            workspace_id
        )

        if workspace is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )

        return workspace

    async def _require_roles(
        self,
        workspace_id: int,
        current_user: User,
        allowed_roles: tuple[WorkspaceMemberRole, ...],
    ) -> None:
        # ADMIN được phép bỏ qua workspace role.
        if current_user.role == UserRole.ADMIN:
            return

        member = await self.member_repo.get_member(
            workspace_id=workspace_id,
            user_id=current_user.id,
        )

        require_workspace_role(
            member,
            *allowed_roles,
        )