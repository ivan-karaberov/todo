from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from .schemas import TaskUpdate, TaskUpdatePartial

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


async def get_task_by_id(
    session: AsyncSession,
    task_id: int
) -> Task:
    return await session.get(Task, task_id)


async def update_task(
    session: AsyncSession,
    task: Task,
    task_update: TaskUpdate | TaskUpdatePartial,
    partial: bool = False
) -> Task:
    for title, body in task_update.model_dump(exclude_unset=partial).items():
        setattr(task, title, body)
    await session.commit()
    return task


async def delete_task(
    session: AsyncSession,
    task: Task
) -> None:
    await session.delete(task)
    await session.commit()