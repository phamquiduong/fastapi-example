# !important: You must load environment variables in the first
from core.load_env import load_env

# Load the environment variables
load_env()


def main():
    import time

    from fastapi import FastAPI

    from auth.router import auth_route
    from core.logging import logger
    from core.roles import create_roles
    from database.config import Base, engine
    from users.router import admin_user_route, user_route

    # Try to connect to the database and create all new tables
    connect_success = False
    while not connect_success:
        try:
            Base.metadata.create_all(bind=engine)
            connect_success = True
            logger.info('Connected to database successfully')
        except Exception:
            logger.error("Connection to database failed.. Try in next 5 seconds")
            time.sleep(5)

    # Create user roles
    create_roles()

    # Create FastAPI application
    app = FastAPI()

    # Include routes
    app.include_router(auth_route)
    app.include_router(user_route)
    app.include_router(admin_user_route)

    return app


# Run the application
app = main()
