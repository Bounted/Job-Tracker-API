from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationPut,
    ApplicationStats,
)
from services.application_service import (
    create_application,
    get_applications_by_user,
    update_application_status,
    delete_application,
    get_application_by_id,
    update_application,
    get_application_stats,
)
from db.session import get_db
from typing import List
from api.deps import get_current_user
from models.user import User
from models.application import ApplicationStatus

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
async def create_application_route(
    application: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await create_application(db, application, current_user.id)  # type: ignore


@router.get("/me", response_model=List[ApplicationRead])
async def get_application_route(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    offset: int = 0,
    limit: int = 10,
):
    return await get_applications_by_user(db, current_user.id, offset, limit)  # type: ignore


@router.get("/stats")
async def get_application_stats_route(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_application_stats(db, current_user.id)  # type: ignore


@router.get("/{application_id}", response_model=ApplicationRead)
async def get_application_by_id_route(
    application_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await get_application_by_id(db, application_id, current_user.id)  # type: ignore


@router.put("/{application_id}", response_model=ApplicationRead)
async def put_application_route(
    application_id: int,
    application: ApplicationPut,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await update_application(db, application_id, application, current_user.id)  # type: ignore


@router.patch("/{application_id}/{state}", response_model=ApplicationRead)
async def patch_status_application_route(
    application_id: int,
    state: ApplicationStatus,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await update_application_status(db, application_id, state, current_user.id)  # type: ignore


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application_router(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_application(db, application_id, current_user.id)  # type: ignore
