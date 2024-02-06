from fastapi import HTTPException, status, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import utils as auth_utils
from .schemas import UserCreate, UserSchema
from core.models import User, db_helper


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def registration(
    session: AsyncSession,
    user_in: UserCreate
) -> User:
    if await session.scalar(select(User).where(User.username==user_in.username)):
        raise HTTPException (
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists!"
        )
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


def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> UserSchema:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error {e}"
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.session_dependency)
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := await get_user_by_username(session, username):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user_not_found"
        )


async def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user)
):
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive"
    )