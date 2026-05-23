from fastapi import Depends
from jose import jwt, JWTError
from typing import Annotated
from core.exceptions import CredentialsError, NotFoundError
from services.user_service import ensure_user_exists
from db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db),
):

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise CredentialsError("Не удалось проверить учетные данные.")

    except JWTError:
        raise CredentialsError("Не удалось проверить учетные данные.")
    try:
        return await ensure_user_exists(db, username)
    except NotFoundError:
        # Все ошибки аутентификации возвращаем как 401.
        # чтобы не раскрывать факт существования пользователя.
        raise CredentialsError("Не удалось проверить учетные данные.")
