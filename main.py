from fastapi import FastAPI
from api.routers import application, user, auth, health
from api.exceptions import (
    not_found_handler,
    already_exists_handler,
    authentication_handler,
    credentials_handler,
    validation_handler,
)
from core.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    AuthenticationError,
    CredentialsError,
)
from fastapi.exceptions import RequestValidationError

app = FastAPI()
app.include_router(application.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(health.router)

app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(AlreadyExistsError, already_exists_handler)
app.add_exception_handler(AuthenticationError, authentication_handler)
app.add_exception_handler(CredentialsError, credentials_handler)
app.add_exception_handler(RequestValidationError, validation_handler)  # type: ignore
