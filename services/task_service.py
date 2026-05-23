from sqlalchemy.ext.asyncio import AsyncSession
from repositories.task_repo import (
    get_tasks_user,
    get_by_id_and_user,
    create,
    update,
    delete,
)
from schemas.task import TaskCreate, TaskPut
from core.exceptions import NotFoundError, AlreadyExistsError
from services.user_service import get_user_by_id
from models.task import TaskStatus
from sqlalchemy.exc import IntegrityError


async def get_task_by_id(db: AsyncSession, task_id: int, user_id: int):
    task = await get_by_id_and_user(db, task_id, user_id)
    if task is None:
        raise NotFoundError("Задачи с таким ID не существует.")
    return task


async def get_tasks_by_user(
    db: AsyncSession, user_id: int, offset: int = 0, limit: int = 10
):
    await get_user_by_id(db, user_id)
    return await get_tasks_user(db, user_id, offset, limit)


async def create_task(db: AsyncSession, task: TaskCreate, user_id: int):
    try:
        return await create(db, task.name, task.content or "", task.state, user_id)
    except IntegrityError:
        raise AlreadyExistsError("Задача с таким именем уже существует.")


async def update_task(db: AsyncSession, task_id: int, task: TaskPut, user_id: int):
    task_repo = await get_by_id_and_user(db, task_id, user_id)
    if task_repo is None:
        raise NotFoundError("Задачи с таким ID не существует.")
    task_repo.name = task.name  # type: ignore
    task_repo.content = task.content  # type: ignore
    task_repo.state = task.state  # type: ignore
    return await update(db, task_repo)


async def update_task_status(
    db: AsyncSession, task_id: int, state: TaskStatus, user_id: int
):
    task = await get_by_id_and_user(db, task_id, user_id)
    if task is None:
        raise NotFoundError("Задачи с таким ID не существует.")
    task.state = state  # type: ignore
    return await update(db, task)


async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> None:
    task = await get_by_id_and_user(db, task_id, user_id)
    if task is None:
        raise NotFoundError("Задачи с таким ID не существует.")
    await delete(db, task_id, user_id)
