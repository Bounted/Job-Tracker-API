from sqlalchemy.orm import Session
from models.task import Task, TaskStatus


def get_tasks_user(db: Session, user_id: int, offset: int = 0, limit: int = 10):
    return (
        db.query(Task).filter(Task.user_id == user_id).offset(offset).limit(limit).all()
    )


def create(db: Session, name: str, content: str, state: TaskStatus, user_id: int):
    new_task = Task(user_id=user_id, name=name, content=content, state=state)
    db.add(new_task)
    db.flush()
    return new_task


def get_by_id_and_user(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()


def update(db: Session, task: Task):
    db.flush()
    return task


def delete(db: Session, task_id: int, user_id: int):
    db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).delete()
    db.flush()
