from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship
from internal.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, index=True, unique=True)
    username = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="user")
    created_at = Column(DateTime, server_default=func.now())