from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.auth.models import RolEnum, DepartmentEnum

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    department: DepartmentEnum

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    rol: RolEnum = RolEnum.USUARIO

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    department: DepartmentEnum | None = None
    rol: RolEnum | None = None

class ChangePassword(BaseModel):
    new_password: str = Field(..., min_length=6, description="Nueva contraseña")    

class ChangePasswordMe(BaseModel):
    old_password: str = Field(..., description="Contraseña actual para verificación")
    new_password: str = Field(..., min_length=6, description="Nueva contraseña")   

class ChangeEmail(BaseModel):
    new_email: EmailStr

class UserResponse(UserBase):
    user_id: int
    rol: RolEnum
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str =  "bearer"

class TokenData(BaseModel):
    user_id: int | None = None
    rol: RolEnum | None = None
    department: DepartmentEnum | None = None

class LoginRequest(BaseModel):
    email: str
    password: str

class PermissionsResponse(BaseModel):
    create: bool
    read: bool
    edited: bool
    delete: bool
    module: list[str]