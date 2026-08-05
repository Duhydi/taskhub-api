from app.models.workspace_member import WorkspaceMember
from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)
from app.repositories.user import UserRepository
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.schemas.workspace_member import (
    WorkspaceMemberCreate,
)


class WorkspaceMemberService:

    def __init__(
        self,
        workspace_repo: WorkspaceRepository,
        user_repo: UserRepository,
        member_repo: WorkspaceMemberRepository,
    ):
        self.workspace_repo = workspace_repo
        self.user_repo = user_repo
        self.member_repo = member_repo

    async def invite_member(
        self,
        workspace_id: int,
        data: WorkspaceMemberCreate,
    ):
        workspace = await self.workspace_repo.get_by_id(
            workspace_id
        )

        if workspace is None:
            raise ValueError("Workspace not found")

        user = await self.user_repo.get_by_id(
            data.user_id
        )

        if user is None:
            raise ValueError("User not found")

        existed = await self.member_repo.get_member(
            workspace_id,
            data.user_id,
        )

        if existed:
            raise ValueError(
                "User already in workspace"
            )

        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=data.user_id,
            role=data.role,
        )

        return await self.member_repo.create(member)

    async def get_members(
        self,
        workspace_id: int,
    ):
        return await self.member_repo.get_members(
            workspace_id
        )

    async def remove_member(
        self,
        workspace_id: int,
        user_id: int,
    ):
        member = await self.member_repo.get_member(
            workspace_id,
            user_id,
        )
        if member.role == WorkspaceMemberRole.OWNER:
            raise ValueError(
                "Workspace owner cannot be removed"
            )
        if member is None:
            raise ValueError("Member not found")

        await self.member_repo.delete(member)