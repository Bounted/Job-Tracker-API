from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="user", cascade="all, delete")
    

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False, unique=True, index=True)
    content = Column(String(1000), nullable=False)
    status = Column(Boolean, default=False)
    user = relationship("User", back_populates="tasks")