from sqlalchemy.ext.asyncio import AsyncSession
from models.refresh_token import RefreshToken
import sqlalchemy
from datetime import datetime
from sqlalchemy.orm import selectinload


async def create_token(
    db: AsyncSession, token: str, user_id: int, expires_at: datetime
):
    db_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(db_token)
    await db.flush()
    return db_token


async def get_by_token(db: AsyncSession, token: str):
    result = await db.execute(
        sqlalchemy.select(RefreshToken)
        .where(RefreshToken.token == token)
        .options(selectinload(RefreshToken.user))
    )
    return result.scalar_one_or_none()


async def delete_token_by_user_id(db: AsyncSession, user_id: int):
    await db.execute(
        sqlalchemy.delete(RefreshToken).where(RefreshToken.user_id == user_id)
    )
    await db.flush()


async def delete_by_token(db: AsyncSession, token: str):
    await db.execute(sqlalchemy.delete(RefreshToken).where(RefreshToken.token == token))
    await db.flush()
