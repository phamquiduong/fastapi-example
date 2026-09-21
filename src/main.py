from fastapi import FastAPI

from errors.handler import handle_error
from routers import users_router

app = FastAPI()

handle_error(app)

app.include_router(users_router)
