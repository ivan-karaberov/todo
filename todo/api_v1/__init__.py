from fastapi import APIRouter

from .tasks.views import router as tasks_router
from .auth.views import router as auth_router

router = APIRouter()

router.include_router(tasks_router, prefix="/tasks", tags=["Task"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])