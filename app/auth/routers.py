from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.auth.models import User
from app.auth.schemas import (
    UserCreate, UserResponse, LoginRequest, ChangePasswordMe, ChangeEmail, PermissionsResponse, Token
)
from app.auth.schemas import TokenData
from app.auth.services import get_user_by_id, get_user_by_email, create_user, authenticate_user
from app.auth.permissions import can_create, can_edit, can_delete, get_accesible_modules
from app.auth.security import get_password_hash, create_access_token, decode_token
from app.core.database import get_db
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    token_data: TokenData = decode_token(token)
    user = get_user_by_id(db, token_data.user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return user

@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(User).all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials or inactive user")
    
    token_data = {
        "user_id": user.user_id,
        "rol": user.rol.value,
        "department": user.department.value
    }
    access_token = create_access_token(data=token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/{user_id}/password", status_code=204)
def change_password(user_id: int, payload: ChangePasswordMe, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not authenticate_user(db, user.email, payload.old_password):
        raise HTTPException(status_code=403, detail="Current password incorrect")
    user.password = get_password_hash(payload.new_password)
    db.commit()
    return

@router.put("/{user_id}/email", status_code=204)
def change_email(user_id: int, payload: ChangeEmail, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if get_user_by_email(db, payload.new_email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user.email = payload.new_email
    db.commit()
    return

@router.get("/{user_id}/permissions", response_model=PermissionsResponse)
def get_permissions(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return PermissionsResponse(
        create=can_create(user),
        read=True,
        edited=can_edit(user),
        delete=can_delete(user),
        module=get_accesible_modules(user)
    )


# ELIMINAR O AGREGAR MANUALMENTE EN EL DATABASE
@router.post("/create-admin-test", status_code=201)
def create_admin_test(db: Session = Depends(get_db)):
    from app.auth.models import RolEnum, DepartmentEnum
    existing_admin = db.query(User).filter(User.rol == RolEnum.ADMINISTRADOR).first()
    if existing_admin:
        return {"message": "Administrator already exists", "email": existing_admin.email}
    admin_user = User(
        email="admin@copymart.com",
        full_name="Administrador CopyMart",
        password=get_password_hash("admin123"),
        rol=RolEnum.ADMINISTRADOR,
        department=DepartmentEnum.ADMINISTRACION,
        is_active=True,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    return {
        "message": "Administrator created successfully",
        "email": admin_user.email,
        "full_name": admin_user.full_name,
        "rol": admin_user.rol,
        "department": admin_user.department
    }