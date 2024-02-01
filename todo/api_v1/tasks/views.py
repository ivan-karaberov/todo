from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_task():
    pass


@router.get("/")
def get_tasks_list():
    pass


@router.patch("/")
def update_task():
    pass


@router.delete("/")
def delete_task():
    pass