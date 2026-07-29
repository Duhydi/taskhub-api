from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TaskHub API"
    version: str = "1.0.0"


settings = Settings()