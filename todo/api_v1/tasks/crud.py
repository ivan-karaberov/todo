from sqlalchemy import select
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


async def get_tasks_list(
    session: AsyncSession,
    user_id: int
) -> list[Task]:
    stmt = (
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.id.desc())
    )
    tasks = await session.scalars(stmt)
    return tasks.all()


async def delete_task(
    session: AsyncSession,
    task: Task
):
    await session.delete(task)
    await session.commit()