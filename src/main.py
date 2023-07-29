from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from auth.routes import auth_route, user_route, users_route
from core.error import ErrorCode, FastAPIException
from core.helper.database_helper import db_helper
from core.schemas.error_schema import ErrorField, ErrorSchema

app = FastAPI()


# Database configuration
db_helper.try_connect()
db_helper.create_all()


# Incluse routers
app.include_router(auth_route)
app.include_router(user_route)
app.include_router(users_route)


# App custom error handlers
@app.exception_handler(FastAPIException)
async def fastapi_exception_handler(_, exc: FastAPIException):
    error, status_code = exc.error_code.get_response()
    error.error_detail = exc.detail
    return JSONResponse(status_code=status_code, content=error.model_dump(exclude_none=True))


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(_, exc: RequestValidationError):
    error, status_code = ErrorCode.ERR_422.get_response()
    error.error_fields = []
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        loc = loc[1:] if loc[0] in ("body", "query", "path") and len(loc) > 1 else loc
        for field in loc:
            error.error_fields.append(ErrorField(field=field, detail=msg))
    return JSONResponse(status_code=status_code, content=error.model_dump(exclude_none=True))


@app.exception_handler(Exception)
async def exception_handler(_, exc: Exception):
    error, status_code = ErrorCode.ERR_500.get_response()
    error.error_detail = str(exc).replace('\n', ' ')
    return JSONResponse(status_code=status_code, content=error.model_dump(exclude_none=True))


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc: HTTPException):
    error = ErrorSchema(error_code=f'ERR_{exc.status_code}', error_message=exc.detail)
    return JSONResponse(status_code=exc.status_code, content=error.model_dump(exclude_none=True))
