from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import sys

from app.core import crud, exceptions
from app.core.dependencies import get_current_user, get_db
from app.models import ImportanceEnum, StatusEnum
from app.schemas import TaskCreate, TaskSchema, TaskEdit


task_router=APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@task_router.post("/task/", response_model=TaskSchema)
async def create_task(
    task: TaskCreate, 
    current_user: str = Depends(get_current_user), 
    db: Session = Depends(get_db)):

    existing_task = crud.check_duplicate_tasks(db, task)
    if existing_task:
        raise exceptions.DuplicatedError("Task already exists")
    db_task = crud.create_user_task(db=db, task=task, user_id = current_user.id)
    
    return jsonable_encoder(db_task)


@task_router.get("/task/", response_model=TaskSchema)
async def get_task(
    task_id: int, 
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):

    db_task = crud.get_task_by_id(db, task_id=task_id)
    if db_task is None:
        raise exceptions.NotFoundError("Task with such ID doesn't exist ")
    if db_task.owner_id != current_user.id:
        raise exceptions.AuthError("No task with such ID for current user")
    
    return jsonable_encoder(db_task)


@task_router.get("/tasks/", response_model = List[TaskSchema])
async def list_tasks(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    
    tasks = crud.list_tasks(db, owner_id = current_user.id)

    if tasks is None:
        raise exceptions.NotFoundError("No Tasks not Found")
    return jsonable_encoder(tasks)


@task_router.get("/tasks/", response_model = List[TaskSchema])
async def list_tasks_by_deadline(
    deadline: datetime = datetime.utcnow().replace(second=0, microsecond=0),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    tasks_by_deadline = crud.list_tasks_by_deadline(
        db, 
        user_id = current_user.id,
        due_before_date = deadline
    )

    if not tasks_by_deadline:
        raise exceptions.NotFoundError(f"No tasks due by {deadline}")
    return jsonable_encoder(tasks_by_deadline)


@task_router.get("/tasks/importance", response_model = List[TaskSchema])
async def list_tasks_by_importance(
    importance: ImportanceEnum,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    tasks_by_importance = crud.list_tasks_by_importance(
        db, 
        user_id=current_user.id, 
        importance=importance
        )

    if not tasks_by_importance:
        raise exceptions.NotFoundError(f"No tasks with *{importance}* importance")
    return jsonable_encoder(tasks_by_importance)


@task_router.get("/tasks/status", response_model = List[TaskSchema])
async def list_tasks_by_status(
    status: StatusEnum,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    tasks_by_status = crud.list_tasks_by_status(
        db, 
        user_id=current_user.id, 
        status=status
        )

    print(tasks_by_status)
    sys.stdout.flush()
    if not tasks_by_status:
        raise exceptions.NotFoundError(f"No tasks with *{status}* status")
    return jsonable_encoder(tasks_by_status)


@task_router.patch("/task/{task_id}", response_model = TaskSchema)
async def update_task(
    task_id: int,
    task_update: TaskEdit,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = crud.get_task_by_id(db, task_id)
    if not db_task:
        raise exceptions.NotFoundError("Task with such ID doesn't exist") 
    
    update_data = task_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return jsonable_encoder(db_task)


@task_router.delete("/task/{task_id}")
async def delete_task(
    task_id: int, 
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    db_task = crud.get_task_by_id(db, task_id)
    if not db_task:
        raise exceptions.NotFoundError("Task with such ID doesn't exist")
    if db_task.owner_id != current_user.id:
        raise exceptions.AuthError("No task with such ID for current user") 
    
    db.delete(db_task)
    db.commit()
    return{"ok": True}