from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.auth.models import User, RolEnum, DepartmentEnum
from app.auth.schemas import UserCreate
from app.auth.security import verify_password, get_password_hash

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.user_id == user_id).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password) or not user.is_active:
        return None
    return user 

def create_user(db: Session, user: UserCreate) -> User:
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registrado")

    db_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        full_name=user.full_name,
        rol=user.rol,
        department=user.department
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user