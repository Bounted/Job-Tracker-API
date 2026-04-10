from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas import TaskCreate, TaskRead, TaskUpdate
from crud import create_task, get_tasks_by_user, update_task_status, delete_task
from database import get_db
from typing import List
from auth import get_current_user
from models import User

router = APIRouter(prefix="/tasks")


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_route(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_task(db, task, current_user.id)


@router.get("/me", response_model=List[TaskRead])
def get_task_user_route(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_tasks_by_user(db, current_user.id)


@router.patch("/", response_model=TaskUpdate)
def patch_task_route(
    task_id: int,
    status: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return update_task_status(db, task_id, status, current_user.id)


@router.delete("/{task_is}", status_code=status.HTTP_200_OK)
def delete_task_router(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return delete_task(db, task_id, current_user.id)
