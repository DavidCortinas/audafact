from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    PORT: int = 8000
    MODEL_PATH: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "models",
        "weights",
    )
    ALLOW_ORIGINS: list = ["*"]
    ENV: str = "development"
    RAPIDAPI_PROXY_SECRET: Optional[str] = None  # Keep as Optional

    @property
    def require_auth(self) -> bool:  # Keep as property
        return self.ENV == "production"

    class Config:
        env_file = ".env"


settings = Settings()
