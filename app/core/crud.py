from sqlalchemy.orm import Session
from datetime import datetime

from app import models, schemas 
from app.core import exceptions, security


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(
        models.UserModel).filter(models.UserModel.username == username
    ).first()


# Only for Admins
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserModel).offset(skip).limit(limit).all()


# Getting and listing tasks
def get_task_by_id(db: Session, task_id: int):
    return db.query(models.TasksModel).filter(models.TasksModel.id == task_id).first()


def list_tasks_by_deadline(db: Session, user_id, due_before_date: datetime):
    current_time = datetime.utcnow()
    tasks = db.query(models.TasksModel).filter(
        models.TasksModel.id == user_id,
        models.TasksModel.deadline >= current_time,
        models.TasksModel.deadline <= due_before_date
    ).all()

    tasks_list=[]
    for task in tasks:
        task_with_deadline= f"Task: {task.taskname}, Deadline: {task.deadline}"
        tasks_list.append(task_with_deadline)

    return tasks_list 


def list_tasks_by_importance(db: Session, user_id, importance: str):
    tasks_importance = db.query(models.TasksModel).filter(
        models.TasksModel.owner_id == user_id,
        models.TasksModel.importance == importance
    ).all()

    return tasks_importance


def list_tasks_by_status(db: Session, user_id, status: str):
    tasks_status = db.query(models.TasksModel).filter(
        models.TasksModel.owner_id == user_id,
        models.TasksModel.status == status
    ).all()

    return tasks_status


def list_tasks(db: Session, owner_id: int):
    return db.query(
        models.TasksModel).filter(models.TasksModel.owner_id == owner_id
    ).all()


def check_duplicate_tasks(db: Session, task: schemas.TaskBase):
    name = db.query(
        models.TasksModel).filter(models.TasksModel.taskname == task.taskname
    ).first()
    due = db.query(
        models.TasksModel).filter(models.TasksModel.deadline == task.deadline
    ).first()

    if name and due:
        return True
    
    return False
        

# Create a User
def create_user(db: Session, user: schemas.UserBaseWithPassword):
    hashed_password = security.hash_password(user.password)
    db_user = models.UserModel(
        firstname = user.firstname,
        lastname = user.lastname,
        username = user.username, 
        email = user.email, 
        hashed_password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Create a Task
def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    try:
        db_task = models.TasksModel(**task.dict(), owner_id = user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    except Exception as e:  # noqa: F841
        db.rollback()
        raise exceptions.ServerError("Error creating a task")
    
