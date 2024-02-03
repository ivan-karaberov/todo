from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models import db_helper

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
def get_tasks_list():
    pass


@router.patch("/")
def update_task():
    pass


@router.delete("/")
def delete_task():
    pass