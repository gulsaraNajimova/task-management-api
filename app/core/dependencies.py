from fastapi import Depends
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import security, crud
from app.core.exceptions import AuthError
from app.core.database import Base, engine, SessionLocal
from app.schemas import Payload, UserSchema
from app.models import UserType

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), 
        token: str = Depends(security.JWTBearer())
    ):
    try:
        payload = jwt.decode(
            token, 
            security.SECRET_KEY, 
            algorithms = security.ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError): 
        raise AuthError("Could not validate credentials")
    
    current_user = crud.get_user_by_id(db, token_data.id)
 
    if not current_user:
        raise AuthError("User not found")
    return current_user


def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
    if not current_user.is_active:
        raise AuthError("Inactive User")
    return current_user


def get_current_superuser(current_user: UserSchema = Depends(get_current_user)):
    if not current_user.is_active:
        raise AuthError("Inactive User")
    if current_user.type != UserType.ADMIN:
        raise AuthError("Not a superuser")
    return current_user

