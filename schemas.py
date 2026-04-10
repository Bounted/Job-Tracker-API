from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    name: str
    content: str
    status: bool = Field(default=False, description="Статус задачи.")


class TaskRead(TaskCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
