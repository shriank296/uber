from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    database_url: str
    migration_database_url: str


settings = AppSettings()
