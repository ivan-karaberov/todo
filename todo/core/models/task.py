from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixin import UserRelationMixin


class Task(Base, UserRelationMixin):
    _user_back_populates = "tasks"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default=""
    )
