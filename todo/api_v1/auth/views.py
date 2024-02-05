from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, utils as auth_utils
from core.models import db_helper
from .schemas import UserCreate, UserSchema, TokenInfo

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


@router.post("/login", response_model=TokenInfo)
def auth_user(
    user: UserSchema = Depends(crud.validate_auth_user)
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    access_token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer"
    )