from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():
    """Liveness probe — проверяет, что сервер жив."""
    return {"status": "alive"}


@router.get("/ready")
async def ready(db: AsyncSession = Depends(get_db)):
    """Readiness probe — проверяет, что БД доступна."""
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        return {"status": "not ready", "database": "unavailable"}
