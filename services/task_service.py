from sqlalchemy.orm import Session
from repositories.task_repo import (
    get_tasks_user,
    get_by_id_and_user,
    create,
    update,
    delete,
)
from schemas.task import TaskCreate
from core.exceptions import NotFoundError, AlreadyExistsError
from services.user_service import get_user_by_id
from models.task import TaskStatus
from sqlalchemy.exc import IntegrityError


def get_tasks_by_user(db: Session, user_id: int, offset: int = 0, limit: int = 10):
    get_user_by_id(db, user_id)
    return get_tasks_user(db, user_id, offset, limit)


def create_task(db: Session, task: TaskCreate, user_id: int):
    try:
        return create(db, task.name, task.content or "", task.state, user_id)
    except IntegrityError:
        raise AlreadyExistsError("A task with this name already exists.")


def update_task_status(db: Session, task_id: int, state: TaskStatus, user_id: int):
    task = get_by_id_and_user(db, task_id, user_id)
    if task is None:
        raise NotFoundError("A task with this ID does not exist.")
    task.state = state  # type: ignore
    return update(db, task)


def delete_task(db: Session, task_id: int, user_id: int) -> None:
    task = get_by_id_and_user(db, task_id, user_id)
    if task is None:
        raise NotFoundError("A task with this ID does not exist.")
    delete(db, task_id, user_id)
