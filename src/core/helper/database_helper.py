import time

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.error import ErrorCode, FastAPIException
from core.helper.log_helper import logger
from core.settings import settings


class DatabaseHelper:
    def __init__(self):
        self.__engine = create_engine(settings.sqlalchemy_database_url)
        self.__base = declarative_base()
        self.__session = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

    def get_session(self):
        return self.__session

    def get_base(self):
        return self.__base

    def create_all(self):
        self.__base.metadata.create_all(bind=self.__engine)

    def is_connected(self) -> bool:
        try:
            self.exec_query('SELECT 1')
            return True
        except FastAPIException as error:
            logger.error(error.detail)
            return False

    def try_connect(self) -> None:
        while not self.is_connected():
            logger.error('Connect database fail. Try in next 10s.....')
            time.sleep(10)

    def exec_query(self, query: str):
        try:
            with self.__session() as session:
                return session.execute(text(query))
        except Exception as error:
            raise FastAPIException(ErrorCode.DB_5001, detail=str(error)) from error


db_helper = DatabaseHelper()
