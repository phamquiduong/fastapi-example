import time

from fastapi import FastAPI

from core.load_env import load_env
from core.logging import logger
from database.config import Base, engine

# Load the environment
load_env

# DB migrate
connect_success = False
while not connect_success:
    try:
        Base.metadata.create_all(bind=engine)
        connect_success = True
        logger.info('Connected to database successfully')
    except Exception:
        logger.error("Connection to database failed.. Try in next 5 seconds")
        time.sleep(5)

# Create FastAPI application
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": 'world'}
