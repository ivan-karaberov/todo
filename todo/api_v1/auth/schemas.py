from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=32)]
    password: Annotated[str, Field(min_length=4)]


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    username: Annotated[str, Field(min_length=3, max_length=32)]
    hashed_password: bytes
    is_active: bool = True
    refresh_token: str | None


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
