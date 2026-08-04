from app.models.user import User
from app.models.workspace import Workspace
from app.models.workspace_member import WorkspaceMember
from app.models.workspace_member_enum import WorkspaceMemberRole
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceUpdate,
)


class WorkspaceService:

    def __init__(
        self,
        repo: WorkspaceRepository,
        member_repo: WorkspaceMemberRepository,
    ):
        self.repo = repo
        self.member_repo = member_repo

    async def create(
        self,
        data: WorkspaceCreate,
        current_user: User,
    ):
        workspace = Workspace(
            name=data.name,
            owner_id=current_user.id,
        )

        created_workspace = await self.repo.create(
            workspace
        )

        owner_member = WorkspaceMember(
            workspace_id=created_workspace.id,
            user_id=current_user.id,
            role=WorkspaceMemberRole.OWNER,
        )

        await self.member_repo.create(
            owner_member
        )

        return created_workspace

    async def get_all(self):
        return await self.repo.get_all()

    async def get_by_id(
        self,
        workspace_id: int,
    ):
        workspace = await self.repo.get_by_id(
            workspace_id
        )

        if workspace is None:
            raise ValueError(
                "Workspace not found"
            )

        return workspace

    async def update(
        self,
        workspace_id: int,
        data: WorkspaceUpdate,
        current_user: User,
    ):
        workspace = await self.get_by_id(
            workspace_id
        )

        if workspace.owner_id != current_user.id:
            raise ValueError(
                "Permission denied"
            )

        workspace.name = data.name

        return await self.repo.update(
            workspace
        )

    async def delete(
        self,
        workspace_id: int,
        current_user: User,
    ):
        workspace = await self.get_by_id(
            workspace_id
        )

        if workspace.owner_id != current_user.id:
            raise ValueError(
                "Permission denied"
            )

        await self.repo.delete(
            workspace
        )