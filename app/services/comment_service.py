from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.rbac import require_workspace_role
from app.models.comment import Comment
from app.models.user import User, UserRole
from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)
from app.repositories import task_repository
from app.repositories.comment_repository import (
    CommentRepository,
)
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
)


class CommentService:

    def __init__(
        self,
        repo: CommentRepository,
        project_repo: ProjectRepository,
        member_repo: WorkspaceMemberRepository,
        db: AsyncSession,
    ):
        self.repo = repo
        self.project_repo = project_repo
        self.member_repo = member_repo
        self.db = db

    async def create_comment(
        self,
        task_id: int,
        data: CommentCreate,
        current_user: User,
    ):
        task = await self._get_task_or_404(
            task_id
        )

        project = await self._get_project_or_404(
            task.project_id
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

        comment = Comment(
            task_id=task_id,
            author_id=current_user.id,
            content=data.content,
        )

        return await self.repo.create(
            comment
        )

    async def get_comments(
        self,
        task_id: int,
        current_user: User,
    ):
        task = await self._get_task_or_404(
            task_id
        )

        project = await self._get_project_or_404(
            task.project_id
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

        return await self.repo.get_by_task(
            task_id
        )

    async def get_comment(
        self,
        comment_id: int,
    ):
        comment = await self.repo.get_by_id(
            comment_id
        )

        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        return comment

    async def update_comment(
        self,
        comment_id: int,
        data: CommentUpdate,
        current_user: User,
    ):
        comment = await self.get_comment(
            comment_id
        )

        await self._require_comment_workspace_member(
            comment=comment,
            current_user=current_user,
        )

        is_author = (
            comment.author_id == current_user.id
        )
        is_admin = (
            current_user.role == UserRole.ADMIN
        )

        if not is_author and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the comment author can update it",
            )

        comment.content = data.content

        return await self.repo.update(
            comment
        )

    async def delete_comment(
        self,
        comment_id: int,
        current_user: User,
    ) -> None:
        comment = await self.get_comment(
            comment_id
        )

        if current_user.role == UserRole.ADMIN:
            await self.repo.delete(comment)
            return

        task = await self._get_task_or_404(
            comment.task_id
        )

        project = await self._get_project_or_404(
            task.project_id
        )

        member = await self.member_repo.get_member(
            workspace_id=project.workspace_id,
            user_id=current_user.id,
        )

        require_workspace_role(
            member,
            WorkspaceMemberRole.OWNER,
            WorkspaceMemberRole.EDITOR,
            WorkspaceMemberRole.VIEWER,
        )

        is_author = (
            comment.author_id == current_user.id
        )
        is_owner = (
            member.role == WorkspaceMemberRole.OWNER
        )

        if not is_author and not is_owner:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Only the author or workspace owner "
                    "can delete this comment"
                ),
            )

        await self.repo.delete(
            comment
        )

    async def _require_comment_workspace_member(
        self,
        comment: Comment,
        current_user: User,
    ) -> None:
        if current_user.role == UserRole.ADMIN:
            return

        task = await self._get_task_or_404(
            comment.task_id
        )

        project = await self._get_project_or_404(
            task.project_id
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

    async def _get_task_or_404(
        self,
        task_id: int,
    ):
        task = await task_repository.get_by_id(
            self.db,
            task_id,
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        return task

    async def _get_project_or_404(
        self,
        project_id: int,
    ):
        project = await self.project_repo.get_by_id(
            project_id
        )

        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        return project

    async def _require_roles(
        self,
        workspace_id: int,
        current_user: User,
        allowed_roles: tuple[
            WorkspaceMemberRole,
            ...,
        ],
    ) -> None:
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