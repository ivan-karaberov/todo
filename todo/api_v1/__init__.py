from fastapi import APIRouter

from .tasks.views import router as tasks_router

router = APIRouter()

router.include_router(tasks_router, prefix="/tasks", tags=["Task"])