from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)


class UserRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
