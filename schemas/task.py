from pydantic import BaseModel, ConfigDict, Field
from models.task import TaskStatus


class TaskCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    content: str | None = None
    state: TaskStatus = Field(
        default=TaskStatus.not_ready, description="Статус задачи."
    )


class TaskRead(BaseModel):
    id: int
    name: str
    content: str | None = None
    state: TaskStatus = Field(description="Статус задачи.")
    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    content: str | None = None
    state: TaskStatus | None = None


class TaskPut(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    content: str
    state: TaskStatus