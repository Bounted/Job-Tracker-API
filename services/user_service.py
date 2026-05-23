from sqlalchemy.ext.asyncio import AsyncSession
from core.security import password_hash
from repositories.user_repo import get_by_id, get_by_name, create, delete
from schemas.user import UserCreate
from core.exceptions import NotFoundError, AlreadyExistsError
from sqlalchemy.exc import IntegrityError


async def ensure_user_exists(db: AsyncSession, name: str):
    user = await get_by_name(db, name)
    if user is None:
        raise NotFoundError("Пользователя с таким именем не существует.")
    return user


async def get_user_by_name_or_none(db: AsyncSession, name: str):
    user = await get_by_name(db, name)
    return user


async def get_user_by_id(db: AsyncSession, user_id: int):
    user = await get_by_id(db, user_id)
    if user is None:
        raise NotFoundError("Пользователя с таким ID не существует.")
    return user


async def delete_user(db: AsyncSession, user_id: int):
    await get_user_by_id(db, user_id)
    await delete(db, user_id)


async def create_user(db: AsyncSession, user: UserCreate):
    hashed = password_hash.hash(user.password)
    try:
        user = await create(db, user.name, hashed)
        return user
    except IntegrityError:
        raise AlreadyExistsError("Пользователь с таким именем уже существует.")
