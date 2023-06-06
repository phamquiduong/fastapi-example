from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from auth.router import auth_route
from users.router import admin_user_route, user_route

# Create FastAPI application
app = FastAPI()

# Include routes
app.include_router(auth_route)
app.include_router(user_route)
app.include_router(admin_user_route)


@app.exception_handler(500)
async def internal_exception_handler(_, error: Exception):
    """Custom exception handler

    Args:
        error (Exception): 500 error Exception

    Return:
        JSONResponse: Detail exception, status code 500.
    """
    return JSONResponse(status_code=500, content=jsonable_encoder({"detail": str(error)}))
