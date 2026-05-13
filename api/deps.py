from fastapi import Depends
from jose import jwt, JWTError
from typing import Annotated
from core.exceptions import credentials_exception, NotFoundError
from services.user_service import ensure_user_exists
from db.session import get_db
from sqlalchemy.orm import Session
from core.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    try:
        return ensure_user_exists(db, username)
    except NotFoundError:
        raise credentials_exception
