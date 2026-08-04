from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "TaskHub API"

    version: str = "1.0.0"

    database_url: str

    secret_key: str

    algorithm: str = "HS256"

    access_token_expire_minutes: int = 60

    refresh_token_expire_days: int = 7

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()