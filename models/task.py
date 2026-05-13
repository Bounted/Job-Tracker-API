from db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum

class TaskStatus(str, Enum):
    ready = "ready"
    at_work = "at_work"
    not_ready = "not_ready"


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False, unique=True, index=True)
    content = Column(String(1000), nullable=False)
    state = Column(SQLEnum(TaskStatus), default=TaskStatus.not_ready, nullable=False)
    user = relationship("User", back_populates="tasks")


