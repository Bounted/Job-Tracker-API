from pydantic import BaseModel, ConfigDict, Field
from models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    content: str | None = None
    state: ApplicationStatus = Field(
        default=ApplicationStatus.applied, description="Статус отклика."
    )


class ApplicationRead(BaseModel):
    id: int
    name: str
    content: str | None = None
    state: ApplicationStatus = Field(description="Статус отклика.")
    model_config = ConfigDict(from_attributes=True)


class ApplicationUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    content: str | None = None
    state: ApplicationStatus | None = None


class ApplicationPut(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    content: str
    state: ApplicationStatus

class ApplicationStats(BaseModel):
    total: int
    by_status: dict[ApplicationStatus, int]
