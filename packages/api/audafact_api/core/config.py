from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    PORT: int = 8000
    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH: str
    ALLOW_ORIGINS: List[str] = ["*"]
    ENV: str
    RAPIDAPI_PROXY_SECRET: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.MODEL_PATH = os.path.abspath(os.path.join(
            self.BASE_PATH,
            "models",
            "weights"
        ))
        self.ENV = "development"
        self.RAPIDAPI_PROXY_SECRET = None

    @property
    def require_auth(self) -> bool:
        return self.ENV == "production"

    class Config:
        env_file = ".env"


settings = Settings()
print(f"Debug - Configured MODEL_PATH: {settings.MODEL_PATH}")