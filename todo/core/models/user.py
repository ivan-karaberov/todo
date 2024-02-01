from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .task import Task

class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)

    tasks: Mapped[List["Task"]] = relationship(back_populates="user")