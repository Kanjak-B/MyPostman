from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/app.db"
    request_timeout_seconds: float = 30.0
    history_max_items: int = 500

    class Config:
        env_prefix = "POSTMAN_"


settings = Settings()
