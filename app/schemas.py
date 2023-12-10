from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models import ImportanceEnum, StatusEnum, UserType


# Task Schemas
class TaskBase(BaseModel):
    taskname: str
    description: Optional[str] = None 
    importance: ImportanceEnum = ImportanceEnum.NORMAL
    deadline: datetime
    status: StatusEnum = StatusEnum.INCOMPLETE


class TaskCreate(TaskBase):
    pass

    class Config:
        schema_extra={
            "example": {
                "taskname": "course registration",
                "description": "register for course for 2023 fall semester",
                "importance": "normal",
                "deadline": datetime(2023, 8, 20, 10, 00),
                "status": "incomplete"
            }
        }


class TaskSchema(TaskBase):
    id: int
    owner_id: int


class TaskEdit(BaseModel):
    taskname: Optional[str] = None
    description: Optional[str] = None 
    importance: Optional[ImportanceEnum] = None
    deadline: Optional[datetime] = None
    status: Optional[StatusEnum] = None


# User Schemas
class UserBase(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    username: str
    email: str 
    type: str = UserType.USER


class UserBaseWithPassword(UserBase):
    password: str 

    class Config:
        schema_extra={
            "example": {
                "firstname": "sarah",
                "lastname": "najimova",
                "username": "sarah",
                "email": "sarah@gmail.com",
                "password": "password123"
            }
        }


class UserSchema(UserBase):
    id: int
    is_active: bool
    tasks: list[TaskSchema] = []


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


# Payload
class Payload(BaseModel):
    id: int
    username: str
    email: str
    type: str
