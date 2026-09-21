import os

from sqlalchemy import URL

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg", username=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME
)
