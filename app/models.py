
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notifications"

    id = Column("notif_id", Integer, autoincrement=True, primary_key=True, index=True)
    message = Column("notif_message", String, nullable=False)
    task_id = Column("task_id", Integer, ForeignKey("tasks.task_id"), nullable=False)
    user_id = Column("user_id", Integer, ForeignKey("users.user_id"), nullable=False)
    is_read = Column("notif_is_read", Boolean)
    created_at = Column("notif_created_at", DateTime)

    task = relationship("Task", back_populates="notifications")
    user = relationship("User", back_populates="notifications")

class Task(Base):
    __tablename__ = "tasks"

    id = Column("task_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.user_id"), nullable=False)
    name = Column("task_name", String, nullable=False)
    
    notifications = relationship("Notification", back_populates="task")
    user = relationship("User", back_populates="tasks")

class User(Base):
    __tablename__ = "users"

    id = Column("user_id", Integer, primary_key=True)
    name = Column("user_name", String, nullable=False)

    tasks = relationship("Task", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

