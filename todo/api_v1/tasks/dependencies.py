from typing import Annotated

from fastapi import HTTPException, Path, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models import db_helper, Task

async def task_by_id(
    task_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> Task:
    task = await crud.get_task_by_id(session=session, task_id=task_id)
    if task is not None:
        return task
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found!"
    )