from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.auth.models import RolEnum, DepartmentEnum

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    username: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    rol: RolEnum = RolEnum.USUARIO
    department: DepartmentEnum = DepartmentEnum.ADMINISTRACION

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    username: Optional[str] = None
    rol: Optional[RolEnum] = None
    department: Optional[DepartmentEnum] = None

class ChangePassword(BaseModel):
    new_password: str = Field(..., min_length=6, description="Nueva contraseña")    

class ChangePasswordMe(BaseModel):
    old_password: str = Field(..., description="Contraseña actual para verificación")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña")   

class ChangeEmail(BaseModel):
    new_email: EmailStr

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    full_name: str
    rol: RolEnum
    department: DepartmentEnum
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    rol: Optional[RolEnum] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class PermissionsResponse(BaseModel):
    create: bool
    read: bool
    edited: bool
    delete: bool
    module: list[str]