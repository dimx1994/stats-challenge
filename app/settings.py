"""
File contains different settings used in project.
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_uri: str

    class Config:
        env_prefix = ""
