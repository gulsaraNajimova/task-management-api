from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from sqlalchemy import Enum

from app.core.database import Base

class UserType(str, PyEnum):
    ADMIN="admin"
    USER="user"

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    type = Column(Enum(UserType), default=UserType.USER)

    tasks = relationship("TasksModel", back_populates = "owner")

    def __repr__(self):
        return f"<User {self.username}, email {self.email}>"


class ImportanceEnum(str, PyEnum):
    IMPORTANT = "important"
    NORMAL = "normal"

class StatusEnum(str, PyEnum):
    COMPLETE = "complete"
    INCOMPLETE = "incomplete"

class TasksModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    taskname = Column(String, index=True)
    description = Column(String, nullable=True)
    importance = Column(Enum(ImportanceEnum), default = ImportanceEnum.NORMAL)
    deadline = Column(DateTime)
    status = Column(Enum(StatusEnum), default = StatusEnum.INCOMPLETE)
    owner_id = Column(String, ForeignKey("users.id"))

    owner=relationship("UserModel", back_populates = "tasks")

    def __repr__(self):
        return f"<Task {self.taskname}, deadline {self.deadline}>"