from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    body: str


class TaskCreate(TaskBase):
    title: Annotated[str, Field(min_length=1, max_length=100)]
    body: str | None = None


class TaskUpdate(TaskCreate):
    pass


class TaskUpdatePartial(TaskCreate):
    title: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    body: str | None = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
