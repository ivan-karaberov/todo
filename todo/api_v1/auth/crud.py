from fastapi import HTTPException, status, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import utils as auth_utils
from .schemas import TokenPair
from core.models import User, db_helper
from ..users.schemas import UserCreate, UserSchema
from ..users.crud import create_user, get_user_by_username


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def registration(
    session: AsyncSession,
    user_in: UserCreate
) -> User:
    stmt = (
        select(User)
        .where(User.username == user_in.username)
    )
    if await session.scalar(stmt):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists!"
        )

    user_in.password = auth_utils.hash_password(user_in.password)
    return await create_user(
        session=session,
        user_in=user_in
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
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token error"
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


async def refresh_token(
    session: AsyncSession,
    refresh_token: str
) -> TokenPair:
    payload: dict = get_current_token_payload(refresh_token)
    user: UserSchema = await get_current_auth_user(payload, session)
    active_user: UserSchema = await get_current_active_auth_user(user)

    if active_user.refresh_token == refresh_token:
        tokens: TokenPair = auth_utils.generate_auth_pair_token(user)
        await update_refresh_token_db(
            session=session,
            user=active_user,
            refresh_token=tokens.refresh_token,
        )
        return tokens

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="invalid refresh token"
    )


async def update_refresh_token_db(
    session: AsyncSession,
    user: UserSchema,
    refresh_token: str
):
    """ Updates the refresh_token field of the user """

    user.refresh_token = refresh_token
    await session.commit()
    return refresh_token
