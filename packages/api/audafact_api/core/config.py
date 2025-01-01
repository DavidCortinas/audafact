from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    PORT: int = 8000
    MODEL_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "models",
        "weights",
    )
    # Allow all origins in development, restrict in production
    ALLOW_ORIGINS: list = ["*"]
    ENV: str = "development"
    RAPIDAPI_PROXY_SECRET: Optional[str] = None

    # Database settings
    DATABASE_URL: str = "postgresql://audafact:notasecret@localhost/audafact_db"

    # Spotify settings
    SPOTIFY_CLIENT_ID: Optional[str] = None
    SPOTIFY_CLIENT_SECRET: Optional[str] = None

    # Add Report price
    REPORT_PRICE: float = 29.99

    @property
    def require_auth(self) -> bool:
        return self.ENV == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
