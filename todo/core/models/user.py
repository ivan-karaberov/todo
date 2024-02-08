from typing import TYPE_CHECKING, List

from sqlalchemy import String, Boolean, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .task import Task

class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary)
    refresh_token: Mapped[str | None] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    tasks: Mapped[List["Task"]] = relationship(back_populates="user")