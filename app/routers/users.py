from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.core import crud, exceptions, security
from app.core.dependencies import get_db
from app.schemas import UserSchema, UserBaseWithPassword


user_router=APIRouter(
    prefix="/users",
    tags=["users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@user_router.post("/signup", response_model=UserSchema)
async def sign_up(user: UserBaseWithPassword, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = user.email)
    if db_user:
        raise exceptions.DuplicatedError("Email already registered")
    
    db_username = crud.get_user_by_username(db, username = user.username)
    if db_username:
        raise exceptions.DuplicatedError("Username already exists")

    db_user = crud.create_user(db=db, user=user)
    return jsonable_encoder(db_user)

@user_router.post("/login")
async def login(email: str, password: str,db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = email)

    if not db_user and not security.verify_password(password, db_user.password):
        raise exceptions.NotFoundError("Incorrect email or password")
    
    payload_data = {
        "id": db_user.id,
        "username": db_user.username, 
        "email": email,
        "type": db_user.type
    }
    token = security.create_token(payload_data)
    return token

