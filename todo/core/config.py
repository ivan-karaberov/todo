import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings


load_dotenv()

DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")
DB_NAME = os.getenv("DB_NAME", "")

BASE_DIR = Path(__file__).parent.parent


class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "core" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "core" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()