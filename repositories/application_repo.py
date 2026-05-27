from sqlalchemy.ext.asyncio import AsyncSession
from models.application import Application, ApplicationStatus
import sqlalchemy


async def get_applications_user(
    db: AsyncSession, user_id: int, offset: int = 0, limit: int = 10
):
    application = await db.execute(
        sqlalchemy.select(Application)
        .where(Application.user_id == user_id)
        .offset(offset)
        .limit(limit)
    )
    return application.scalars().all()


async def create(
    db: AsyncSession, name: str, content: str, state: ApplicationStatus, user_id: int
):
    new_application = Application(
        user_id=user_id, name=name, content=content, state=state
    )
    db.add(new_application)
    await db.flush()
    return new_application


async def get_by_id_and_user(db: AsyncSession, application_id: int, user_id: int):
    application = await db.execute(
        sqlalchemy.select(Application).where(
            Application.id == application_id, Application.user_id == user_id
        )
    )
    return application.scalar_one_or_none()


async def update(db: AsyncSession, application: Application):
    await db.flush()
    return application


async def delete(db: AsyncSession, application_id: int, user_id: int):
    await db.execute(
        sqlalchemy.delete(Application).where(
            Application.id == application_id, Application.user_id == user_id
        )
    )
    await db.flush()


async def count_stats(db: AsyncSession, user_id: int):
    result = await db.execute(
        sqlalchemy.select(Application.state, sqlalchemy.func.count(Application.id).label("count"))
        .where(Application.user_id == user_id)
        .group_by(Application.state)
    )
    res = result.all()
    by_status = {r[0]: r[1] for r in res}
    total = sum(i for i in by_status.values())
    return {"total": total, "by_status": by_status}

