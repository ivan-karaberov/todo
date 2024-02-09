from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate
from core.models import User


async def create_user(
    session: AsyncSession,
    user_in: UserCreate
) -> User:
    user = User(
        username=user_in.username,
        hashed_password=user_in.password
    )
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(
    session: AsyncSession,
    username: str
) -> User:
    return await session.scalar(
        select(User)
        .where(User.username == username)
    )
