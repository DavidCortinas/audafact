from pydantic import BaseSettings


class Settings(BaseSettings):
    # ... existing settings ...

    # JWT settings
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200  # 30 days
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 525600  # 1 year

    class Config:
        env_file = ".env"
