from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    hashed_password: bytes
    is_active: bool = True


class TokenInfo(BaseModel):
    access_token: str
    token_type: str