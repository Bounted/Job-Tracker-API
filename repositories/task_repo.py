from sqlalchemy.ext.asyncio import AsyncSession
from models.task import Task, TaskStatus
import sqlalchemy


async def get_tasks_user(
    db: AsyncSession, user_id: int, offset: int = 0, limit: int = 10
):
    task = await db.execute(
        sqlalchemy.select(Task)
        .where(Task.user_id == user_id)
        .offset(offset)
        .limit(limit)
    )
    return task.scalars().all()


async def create(
    db: AsyncSession, name: str, content: str, state: TaskStatus, user_id: int
):
    new_task = Task(user_id=user_id, name=name, content=content, state=state)
    db.add(new_task)
    await db.flush()
    return new_task


async def get_by_id_and_user(db: AsyncSession, task_id: int, user_id: int):
    task = await db.execute(
        sqlalchemy.select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return task.scalar_one_or_none()


async def update(db: AsyncSession, task: Task):
    await db.flush()
    return task


async def delete(db: AsyncSession, task_id: int, user_id: int):
    await db.execute(
        sqlalchemy.delete(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    await db.flush()
