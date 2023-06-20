import sys

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from auth.routes import admin_route, auth_route, user_route
from auth.routes.auth_router import auth_route
from core.schemas.error_schema import (FieldErrorSchema, HTTPExceptionSchema,
                                       RequestValidationErrorSchema)
from database.create_admin_user import create_admin_user
from database.migrate import Migration

# Create FastAPI application
app = FastAPI()


# Include routes
app.include_router(auth_route)
app.include_router(user_route)
app.include_router(admin_route)


# Custom error handler
@app.exception_handler(500)
async def internal_exception_handler(_, error: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=jsonable_encoder(HTTPExceptionSchema(detail=str(error)).__dict__))


@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(request, exc):
    request_validation_error = RequestValidationErrorSchema()

    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        loc = loc[1:] if loc[0] in ("body", "query", "path") and len(loc) > 1 else loc
        for field in loc:
            request_validation_error.fields.append(FieldErrorSchema(name=field, detail=msg))

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(request_validation_error.__dict__)
    )


args = iter(sys.argv[1:])
action = next(args, None)


# Migrate function
if action in ('migrate', '-m'):
    Migration().run()

# Create admin user
if action == 'createsuperuser':
    create_admin_user()
