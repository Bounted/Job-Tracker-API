from fastapi import status, HTTPException


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
authentication_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
class ServiceError(Exception):
    pass
class NotFoundError(ServiceError):
    pass
class AlreadyExistsError(ServiceError):
    pass
