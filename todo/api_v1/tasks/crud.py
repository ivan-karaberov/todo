from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task

async def create_task(
    session: AsyncSession,
    user_id: int,
    task_title: str
)-> Task:
    task = Task(title=task_title, user_id=user_id)
    session.add(task)
    await session.commit()
    return task