from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    username: str
    hashed_password: bytes
    is_active: bool = True
    refresh_token: str | None


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str