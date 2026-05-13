from db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="user", cascade="all, delete")
