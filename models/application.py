from db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum

class ApplicationStatus(str, Enum):
    applied = "applied"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"
    accepted = "accepted"


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False, unique=True, index=True)
    content = Column(String(1000), nullable=False)
    state = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.applied, nullable=False)
    user = relationship("User", back_populates="applications")


