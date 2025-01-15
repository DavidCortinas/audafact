from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path

# Get the base directory of your project
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    # API settings
    PORT: int = 8000
    MODEL_PATH: str = str(BASE_DIR / "models" / "weights")
    ALLOW_ORIGINS: List[str] = ["http://localhost:3000"]
    ENV: str = "development"
    RAPIDAPI_PROXY_SECRET: str = ""
    require_auth: bool = False

    # Database settings
    DATABASE_URL: str = "postgresql://audafact:notasecret@localhost/audafact_db"

    # Spotify settings
    SPOTIFY_CLIENT_ID: Optional[str] = None
    SPOTIFY_CLIENT_SECRET: Optional[str] = None

    # Report settings
    REPORT_PRICE: float = 29.99

    # Redis settings
    REDIS_URL: str = "redis://localhost:6379"

    # Email settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "mail.privateemail.com"

    # JWT settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()
