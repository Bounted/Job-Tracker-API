from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.task import TaskCreate, TaskRead
from services.task_service import (
    create_task,
    get_tasks_by_user,
    update_task_status,
    delete_task,
)
from db.session import get_db
from typing import List
from api.deps import get_current_user
from models.user import User
from models.task import TaskStatus
from core.exceptions import AlreadyExistsError, NotFoundError

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task_route(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await create_task(db, task, current_user.id)
    except AlreadyExistsError as a:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(a))


@router.get("/me", response_model=List[TaskRead])
async def get_task_route(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    offset: int = 0,
    limit: int = 10,
):
    return await get_tasks_by_user(db, current_user.id, offset, limit)


@router.patch("/{task_id}/{state}", response_model=TaskRead)
async def patch_status_task_route(
    task_id: int,
    state: TaskStatus,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await update_task_status(db, task_id, state, current_user.id)
    except NotFoundError as n:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(n))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_router(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await delete_task(db, task_id, current_user.id)
    except NotFoundError as n:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(n))
