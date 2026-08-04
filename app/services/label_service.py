from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app.dependencies.rbac import require_workspace_role
from app.models.label import Label
from app.models.user import User, UserRole
from app.models.workspace_member_enum import (
    WorkspaceMemberRole,
)
from app.repositories import task_repository
from app.repositories.label_repository import (
    LabelRepository,
)
from app.repositories.project_repository import (
    ProjectRepository,
)
from app.repositories.workspace_member_repository import (
    WorkspaceMemberRepository,
)
from app.schemas.label import (
    LabelCreate,
    LabelUpdate,
)


class LabelService:

    def __init__(
        self,
        label_repo: LabelRepository,
        project_repo: ProjectRepository,
        member_repo: WorkspaceMemberRepository,
        db,
    ):
        self.label_repo = label_repo
        self.project_repo = project_repo
        self.member_repo = member_repo
        self.db = db

    async def create_label(
        self,
        project_id: int,
        data: LabelCreate,
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

        label = Label(
            project_id=project_id,
            name=data.name,
            color=data.color,
        )

        try:
            return await self.label_repo.create(
                label
            )
        except IntegrityError:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Label name already exists "
                    "in this project"
                ),
            )

    async def get_labels(
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

        return await self.label_repo.get_by_project(
            project_id
        )

    async def get_label(
        self,
        label_id: int,
    ):
        label = await self.label_repo.get_by_id(
            label_id
        )

        if label is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found",
            )

        return label

    async def update_label(
        self,
        label_id: int,
        data: LabelUpdate,
        current_user: User,
    ):
        label = await self.get_label(
            label_id
        )

        project = await self._get_project_or_404(
            label.project_id
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
            setattr(
                label,
                field,
                value,
            )

        try:
            return await self.label_repo.update(
                label
            )
        except IntegrityError:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Label name already exists "
                    "in this project"
                ),
            )

    async def delete_label(
        self,
        label_id: int,
        current_user: User,
    ) -> None:
        label = await self.get_label(
            label_id
        )

        project = await self._get_project_or_404(
            label.project_id
        )

        await self._require_roles(
            workspace_id=project.workspace_id,
            current_user=current_user,
            allowed_roles=(
                WorkspaceMemberRole.OWNER,
                WorkspaceMemberRole.EDITOR,
            ),
        )

        await self.label_repo.delete(
            label
        )

    async def assign_label(
        self,
        task_id: int,
        label_id: int,
        current_user: User,
    ):
        task = await self._get_task_or_404(
            task_id
        )

        label = await self.get_label(
            label_id
        )

        if task.project_id != label.project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Task and label must belong "
                    "to the same project"
                ),
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
            ),
        )

        if label in task.labels:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Label already assigned to task",
            )

        task.labels.append(label)

        await self.db.commit()
        await self.db.refresh(task)

        return {
            "message": "Label assigned successfully",
        }

    async def remove_label(
        self,
        task_id: int,
        label_id: int,
        current_user: User,
    ):
        task = await self._get_task_or_404(
            task_id
        )

        label = await self.get_label(
            label_id
        )

        if task.project_id != label.project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "Task and label must belong "
                    "to the same project"
                ),
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
            ),
        )

        if label not in task.labels:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label is not assigned to task",
            )

        task.labels.remove(label)

        await self.db.commit()

        return {
            "message": "Label removed successfully",
        }

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