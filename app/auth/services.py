from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from auth.models import User, RolEnum, DepartmentEnum
from auth.schemas import UserCreate
from auth.security import verify_password, get_password_hash

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

    # Asegurar que permissions sea un dict válido
    perms_data = user.permissions if user.permissions else {}
    
    # Generar username si no se proporciona (usar email sin @dominio)
    username_value = user.username if user.username else user.email.split('@')[0]
    
    db_user = User(
        email=user.email,
        username=username_value,
        password=get_password_hash(user.password),
        full_name=user.full_name,
        rol=user.rol,
        department=user.department,
        permissions=perms_data
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating user: {str(e)}")
