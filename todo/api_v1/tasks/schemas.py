from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    body: str


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskCreate):
    pass


class TaskUpdatePartial(TaskCreate):
    title: str | None = None
    body: str | None = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
