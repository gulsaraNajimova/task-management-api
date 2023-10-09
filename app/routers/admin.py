from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List

from app.core import crud, exceptions

from app.schemas import UserSchema, TaskSchema
from app.core.dependencies import get_db, get_current_superuser


admin_router=APIRouter(
    prefix="/admin",
    tags=["admin"]
)


# Only for Admin
@admin_router.get("/users", response_model = List[UserSchema])
async def get_users(
    skip: int = 0, 
    limit: int = 100, 
    current_user: str = Depends(get_current_superuser),
    db: Session = Depends(get_db)
    ):
    users = crud.get_users(db, skip=skip, limit=limit)
    return jsonable_encoder(users)
   


@admin_router.get("/{user_id}/tasks", response_model = List[TaskSchema])
async def get_user_tasks(
    user_id: int, 
    current_user: str = Depends(get_current_superuser),
    db: Session = Depends(get_db)
    ):

    db_user = crud.get_user_by_id(db, user_id = user_id)
    if db_user is None:
        raise exceptions.NotFoundError("No User with such ID")
    
    user_tasks = crud.list_tasks(db, owner_id = user_id)

    if user_tasks is None:
        raise exceptions.NotFoundError("No Task not Found for this user")
    return jsonable_encoder(user_tasks)
    