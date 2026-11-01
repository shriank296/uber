from functools import lru_cache

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    database_url: str
    migration_database_url: str
    project_name: str = "Uber"


@lru_cache
def get_app_settings():
    return AppSettings()
