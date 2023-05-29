import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__USERNAME = os.getenv('MYSQL_USER')
__PASSWORD = os.getenv('MYSQL_PASSWORD')
__HOST = os.getenv('MYSQL_HOST')
__PORT = os.getenv('MYSQL_PORT')
__DBNAME = os.getenv('MYSQL_DATABASE')

__SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{__USERNAME}:{__PASSWORD}@{__HOST}:{__PORT}/{__DBNAME}"

engine = create_engine(__SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
