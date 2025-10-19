from typing import Optional
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Backend API"
    debug: bool = True
    sqlite_db_file: str = "app.db"
    database_url: Optional[str] = None
    jwt_secret_key: str = "CHANGE_ME_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # pydantic-settings v2 configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def sqlmodel_database_uri(self) -> str:
        if self.database_url:
            return self.database_url
        # Default to SQLite file located in the backend directory (stable absolute path)
        backend_dir = Path(__file__).resolve().parents[2]
        db_path = backend_dir / self.sqlite_db_file
        return f"sqlite:///{db_path}"


settings = Settings()



