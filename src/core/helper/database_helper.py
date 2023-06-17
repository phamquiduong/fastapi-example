import time

from sqlalchemy import create_engine, exc, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.helper.log_helper import logger
from core.settings import settings


class __DatabaseHelper:
    def __init__(self, sqlalchemy_database_url: str) -> None:
        self.sqlalchemy_database_url = sqlalchemy_database_url

        self.__engine = create_engine(sqlalchemy_database_url)
        self.__Session = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)

        self.__Base = declarative_base()

    def is_connect(self) -> bool:
        try:
            self.exec_query('SELECT 1')
            return True
        except exc.SQLAlchemyError as error:
            logger.error(str(error))
            return False

    def try_connect(self) -> None:
        while not self.is_connect():
            logger.error('Connect database fail. Try in next 5s.....')
            time.sleep(5)

    def get_session(self):
        return self.__Session

    def get_base(self):
        return self.__Base

    def exec_query(self, query: str):
        with self.__Session() as session:
            session.execute(text(query))


database_helper = __DatabaseHelper(
    sqlalchemy_database_url=settings.sqlalchemy_database_url
)
