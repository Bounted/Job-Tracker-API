from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
import sqlalchemy


async def get_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(sqlalchemy.select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_by_name(db: AsyncSession, name: str):
    result = await db.execute(sqlalchemy.select(User).where(User.name == name))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, name: str, hashed_password: str):
    user = User(name=name, hashed_password=hashed_password)
    db.add(user)
    await db.flush()
    return user


async def delete(db: AsyncSession, user_id: int):
    await db.execute(sqlalchemy.delete(User).where(User.id == user_id))
    await db.flush()
