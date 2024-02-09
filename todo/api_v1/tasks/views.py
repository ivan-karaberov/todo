from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models import db_helper
from .dependencies import task_by_id
from .schemas import Task, TaskUpdatePartial
from ..users.schemas import UserSchema
from ..auth.crud import get_current_active_auth_user

router = APIRouter()


@router.post("/")
async def create_task(
    task_title: str,
    user: UserSchema = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.create_task(
        session=session,
        user_id=user.id,
        task_title=task_title
    )


@router.get("/")
async def get_tasks_list(
    user: UserSchema = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_tasks_list(
        session=session,
        user_id=user.id
    )


@router.patch("/", status_code=204)
async def update_task(
    task_update: TaskUpdatePartial,
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.update_task(
        session=session,
        task=task,
        task_update=task_update,
        partial=True
    )


@router.delete("/", status_code=204)
async def delete_task(
    task: Task = Depends(task_by_id),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.delete_task(
        session=session,
        task=task
    )
