from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import utils as auth_utils
from .schemas import UserCreate
from core.models import User


async def registration(
    session: AsyncSession,
    user_in: UserCreate
) -> User:
    if await session.scalar(select(User).where(User.username==user_in.username)):
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists!"
        )
    print(auth_utils.hash_password(user_in.password))
    user = User(
        username=user_in.username,
        hashed_password=auth_utils.hash_password(user_in.password)
    )
    session.add(user)
    await session.commit()
    return user 
    