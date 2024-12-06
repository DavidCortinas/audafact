from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PORT: int = 8000
    MODEL_PATH: str = "models"
    ALLOW_ORIGINS: list = ["*"]
    ENV: str = "development"
    RAPIDAPI_PROXY_SECRET: Optional[str] = None

    @property
    def require_auth(self) -> bool:
        return self.ENV == "production"

    class Config:
        env_file = ".env"

settings = Settings()