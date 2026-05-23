from fastapi import Request
from fastapi.responses import JSONResponse
from core.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    AuthenticationError,
    CredentialsError,

)
from schemas.error import ErrorResponse
from fastapi.exceptions import RequestValidationError


async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error_code="NOT_FOUND",
            message=str(exc),
        ).model_dump(),
    )


async def already_exists_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=409,
        content=ErrorResponse(
            error_code="ALREADY_EXISTS",
            message=str(exc),
        ).model_dump(),
    )


async def authentication_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=401,
        content=ErrorResponse(
            error_code="UNAUTHORIZED",
            message=str(exc),
        ).model_dump(),
        headers={"WWW-Authenticate": "Bearer"},
    )


async def credentials_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=401,
        content=ErrorResponse(
            error_code="UNAUTHORIZED",
            message=str(exc),
        ).model_dump(),
        headers={"WWW-Authenticate": "Bearer"},
    )


async def validation_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            success=False,
            error_code="VALIDATION_ERROR",
            message="Ошибка валидации входных данных",
        ).model_dump(),
    )
