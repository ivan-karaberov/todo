from typing import Annotated

from fastapi import HTTPException, Path, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models import db_helper, Task
from ..users.schemas import UserSchema
from ..auth.crud import get_current_active_auth_user


async def task_by_id(
    task_id: Annotated[int, Path],
    user: UserSchema = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> Task:
    """ Getting authorized user's task from db by task_id """

    task = await crud.get_task_by_id(session=session, task_id=task_id)

    if task and task.user_id == user.id:
        return task

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found!"
    )
