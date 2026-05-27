from sqlalchemy.ext.asyncio import AsyncSession
from repositories.application_repo import (
    get_applications_user,
    get_by_id_and_user,
    create,
    update,
    delete,
    count_stats,
)
from schemas.application import ApplicationCreate, ApplicationPut
from core.exceptions import NotFoundError, AlreadyExistsError
from services.user_service import get_user_by_id
from models.application import ApplicationStatus
from sqlalchemy.exc import IntegrityError


async def get_application_by_id(db: AsyncSession, application_id: int, user_id: int):
    application = await get_by_id_and_user(db, application_id, user_id)
    if application is None:
        raise NotFoundError("Отклика с таким ID не существует.")
    return application


async def get_applications_by_user(
    db: AsyncSession, user_id: int, offset: int = 0, limit: int = 10
):
    await get_user_by_id(db, user_id)
    return await get_applications_user(db, user_id, offset, limit)


async def create_application(
    db: AsyncSession, application: ApplicationCreate, user_id: int
):
    try:
        return await create(
            db, application.name, application.content or "", application.state, user_id
        )
    except IntegrityError:
        raise AlreadyExistsError("Отклика с таким именем уже существует.")


async def update_application(
    db: AsyncSession, application_id: int, application: ApplicationPut, user_id: int
):
    app_repo = await get_by_id_and_user(db, application_id, user_id)
    if app_repo is None:
        raise NotFoundError("Отклика с таким ID не существует.")
    app_repo.name = application.name  # type: ignore
    app_repo.content = application.content  # type: ignore
    app_repo.state = application.state  # type: ignore
    return await update(db, app_repo)


async def update_application_status(
    db: AsyncSession, application_id: int, state: ApplicationStatus, user_id: int
):
    application = await get_by_id_and_user(db, application_id, user_id)
    if application is None:
        raise NotFoundError("Отклика с таким ID не существует.")
    application.state = state  # type: ignore
    return await update(db, application)


async def delete_application(
    db: AsyncSession, application_id: int, user_id: int
) -> None:
    application = await get_by_id_and_user(db, application_id, user_id)
    if application is None:
        raise NotFoundError("Отклика с таким ID не существует.")
    await delete(db, application_id, user_id)


async def get_application_stats(db: AsyncSession, user_id: int):
    return await count_stats(db, user_id)
