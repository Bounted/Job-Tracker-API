from sqlalchemy.orm import Session
from models import User, Task
from schemas import *
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def create_user(db: Session, user: UserCreate):
    hashed = password_hash.hash(user.password)
    user = User(name=user.name, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user


def get_tasks_by_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()


def create_task(db: Session, task: TaskCreate, user_id: int):
    tasks = Task(user_id=user_id, name=task.name, content=task.content, status=task.status)
    db.add(tasks)
    db.commit()
    db.refresh(tasks)
    return tasks


def update_task_status(db: Session, task_id: int, status: bool, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        task.status = status
        db.commit()
        db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
