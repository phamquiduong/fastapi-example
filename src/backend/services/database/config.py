import os
import time

from sqlalchemy import create_engine, exc, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.logging import logger

SQLALCHEMY_ECHO_MAP = {
    'none': None,
    'false': False,
    'true': True,
    'debug': 'debug',
}


SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL') \
    or "mysql+mysqlconnector://{user}:{pw}@{host}:{port}/{db_name}".format(
        user=os.getenv('MYSQL_USER'),
        pw=os.getenv('MYSQL_PASSWORD'),
        host=os.getenv('MYSQL_HOST'),
        port=os.getenv('MYSQL_PORT'),
        db_name=os.getenv('MYSQL_DATABASE'))

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       echo_pool=SQLALCHEMY_ECHO_MAP[os.getenv('SQLALCHEMY_LOG_LEVEL').lower()])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def try_connection():
    """Try to connect to the database. If connect fail try in next 5 seconds.
    """

    is_connected = False
    while not is_connected:
        try:
            with SessionLocal() as session:
                session.execute(text('SELECT 1'))
            logger.info("Connect to database successfully")
            is_connected = True
        except exc.SQLAlchemyError:
            logger.error("Connect to database failed.. Try again after 5 seconds")
            time.sleep(5)
