from fastapi import HTTPException, status, Form, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import utils as auth_utils
from .schemas import UserCreate
from core.models import User, db_helper


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


async def get_user_by_username(
    session: AsyncSession,
    username: str
) -> User:
    return await session.scalar(
        select(User)
        .where(User.username == username)
    )


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    unauthed_ext = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password"
    )

    if not (user := await get_user_by_username(session, username)):
        raise unauthed_ext
    
    if not auth_utils.validate_password(
        password=password,
        hashed_password=user.hashed_password
    ):
        raise unauthed_ext
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive"
        )
    
    return user