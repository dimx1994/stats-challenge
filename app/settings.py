from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_uri: str = "postgresql://user:password@db:5432/stats"
    click_through_window_seconds: int = 300

    class Config:
        env_prefix = ""
