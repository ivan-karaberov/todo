from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models import db_helper
from .dependencies import task_by_id
from .schemas import Task, TaskUpdatePartial

router = APIRouter()


@router.post("/")
async def create_task(
    user_id: int,
    task_title: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.create_task(
        session=session, 
        user_id=user_id,
        task_title=task_title
    )


@router.get("/")
async def get_tasks_list(
    user_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.get_tasks_list(
        session=session, 
        user_id=user_id
    )


@router.patch("/")
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


@router.delete("/")
def delete_task():
    pass