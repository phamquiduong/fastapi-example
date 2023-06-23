import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import quote_plus

from pydantic import BaseSettings

from core.helper.env_helper import load_env

# Load enviroment variables
load_env(env_file='.env')


SQLALCHEMY_DATABASE_URL = 'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}'


class __Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent.parent
    password_salt = os.getenv('PASSWORD_SALT') or ''

    # jwt settings
    secret_key: str = os.getenv('SECRET_KEY') or 'not_secret'
    algorithm: str = os.getenv('ALGORITHM') or 'HS256'

    access_token_exp: timedelta = timedelta(minutes=15)
    refresh_token_exp: timedelta = timedelta(days=60)

    # Logging settings
    log_dir: Path = base_dir / '../log'
    log_level: str = os.getenv('LOG_LEVEL') or 'DEBUG'
    log_format: str = '[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s'
    log_time_format: str = '%y-%m-%d %h:%m:%s'
    log_handlers: list[str] = os.getenv('LOG_HANDLER', '').split(',') or ['console']

    # Databse config
    sqlalchemy_database_url: str = (os.getenv('SQLALCHEMY_DATABASE_URL')
                                    or SQLALCHEMY_DATABASE_URL.format(
                                        user=quote_plus(os.getenv('MYSQL_USER')),
                                        password=quote_plus(os.getenv('MYSQL_PASSWORD')),
                                        host=quote_plus(os.getenv('MYSQL_HOST')),
                                        port=quote_plus(os.getenv('MYSQL_PORT')),
                                        db_name=quote_plus(os.getenv('MYSQL_DATABASE')),
    ))
    migrations_folder: str = os.getenv('MIGRATIONS_FOLDER') or 'sqlite'

    # Role configuration
    default_role = 'user'


settings = __Settings()
