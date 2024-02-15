from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task
from .schemas import TaskCreate, TaskUpdate, TaskUpdatePartial


async def create_task(
    session: AsyncSession,
    user_id: int,
    task_in: TaskCreate
) -> Task:
    task = Task(
        title=task_in.title,
        body=task_in.body,
        user_id=user_id
    )
    session.add(task)
    await session.commit()
    return task


async def get_tasks_list(
    session: AsyncSession,
    user_id: int
) -> list[Task]:
    tasks = await session.scalars(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.id.desc())
    )
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
) -> str:
    await session.delete(task)
    await session.commit()
    return "task delete successfully"
