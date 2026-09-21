from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from errors.api_exception import APIException
from schemas.error import ErrorResponse, FieldError


def handle_error(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        fields: list[FieldError] = [
            FieldError(
                name=error["loc"][-1] if isinstance(error["loc"][-1], str) else "__all__",
                message=error["msg"],
                type=error["type"],
                input=error["input"],
                context=error["ctx"],
            )
            for error in exc.errors()
        ]

        err_res = ErrorResponse(
            status=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Unprocessable Content.", fields=fields
        )
        return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status)

    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        err_res = ErrorResponse(status=exc.status_code, detail=exc.detail, fields=exc.fields)
        return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status, headers=exc.headers)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        err_res = ErrorResponse(status=exc.status_code, detail=exc.detail)
        return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status, headers=exc.headers)

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        err_res = ErrorResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error.")
        return JSONResponse(err_res.model_dump(exclude_none=True), status_code=err_res.status)
