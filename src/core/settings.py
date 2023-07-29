import os
from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    base_dir: Path = Path(__file__).resolve().parent.parent
    password_salt: str = os.getenv('PASSWORD_SALT', '')

    # jwt settings
    secret_key: str = os.getenv('SECRET_KEY', '')
    algorithm: str = os.getenv('ALGORITHM', '')

    access_token_exp: timedelta = timedelta(minutes=15)
    refresh_token_exp: timedelta = timedelta(days=60)

    # Logging settings
    log_dir: Path = base_dir / '../log'
    log_level: str = os.getenv('LOG_LEVEL') or 'DEBUG'
    log_format: str = '[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s'
    log_time_format: str = '%y-%m-%d %h:%m:%s'
    log_handlers: list[str] = os.getenv('LOG_HANDLER', '').split(',') or ['console']

    # Databse config
    sqlalchemy_database_url: str = 'sqlite:///../database/db.sqlite3'

    # Pagination settings
    limit: int = 10


settings = Settings()
