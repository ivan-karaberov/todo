from fastapi import APIRouter, Depends

from . import crud
from .schemas import UserCreate
from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

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