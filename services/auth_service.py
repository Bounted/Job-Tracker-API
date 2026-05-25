from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta, datetime, timezone
from core.security import (
    verify_password,
    create_access_token,
    DUMMY_HASH,
    create_refresh_token,
)
from services.user_service import get_user_by_name_or_none
from core.config import settings
from repositories.token_repo import create_token, get_by_token, delete_by_token, delete_token_by_user_id
from core.exceptions import AuthenticationError
from jose import jwt

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_name_or_none(db, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def login(db: AsyncSession, username: str, password: str):
    user = await authenticate_user(db, username, password)
    if not user:
        return None
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_access = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    access = create_access_token(
        data={"sub": user.name},
        expires_delta=access_token_expires,
    )
    refresh = create_refresh_token(
        data={"sub": user.name},
        expires_delta=refresh_token_access,
    )
    payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    exp = payload["exp"]
    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
    await create_token(db, refresh, user.id, expires_at)  #type: ignore
    return access, refresh



async def refresh_access_token(db: AsyncSession, refresh: str):
    r_token = await get_by_token(db, refresh)
    if not r_token:
        raise AuthenticationError("Refresh токен отсутствует.")
    expires_at = r_token.expires_at.replace(tzinfo=timezone.utc) if r_token.expires_at.tzinfo is None else r_token.expires_at
    if expires_at < datetime.now(timezone.utc):  #type: ignore
        await delete_by_token(db, refresh)
        raise AuthenticationError("Refresh токен устарел.")
    await delete_by_token(db, refresh)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_access = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    access = create_access_token(
        data={"sub": r_token.user.name},
        expires_delta=access_token_expires,
    )
    refresh = create_refresh_token(
        data={"sub": r_token.user.name},
        expires_delta=refresh_token_access,
    )
    payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    exp = payload["exp"]
    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)    
    await create_token(db, refresh, r_token.user_id, expires_at)  #type: ignore
    return access, refresh


async def logout_service(db: AsyncSession, user_id: int):
    await delete_token_by_user_id(db, user_id)  