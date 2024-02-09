from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from core.models import db_helper
from .schemas import UserCreate, UserSchema, TokenPair

router = APIRouter()


@router.post("/registration")
async def registration(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    await crud.registration(
        session=session,
        user_in=user_in
    )
    return "user created successfully"


@router.post("/login", response_model=TokenPair)
async def auth_user(
    user: UserSchema = Depends(crud.validate_auth_user),
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    tokens: TokenPair = crud.generate_auth_pair_token(user)
    await crud.update_refresh_token_db(
        session=session,
        user=user,
        refresh_token=tokens.refresh_token
    )
    return tokens


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(
    refresh_token: str,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    return await crud.refresh_token(
        session=session,
        refresh_token=refresh_token
    )
