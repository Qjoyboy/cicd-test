from sqlalchemy import Column, ForeignKey, Integer, Boolean, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import relationship
from internal.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")
    created_at = Column(DateTime, server_default=func.now())
