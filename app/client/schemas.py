from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from ..contact.schemas import ContactRead

class AreaCreate(BaseModel):
    branch_id: int
    name: str


class AreaUpdate(BaseModel):
    name: Optional[str] = None

class AreaResponse(BaseModel):
    area_id: int
    name: str
    created_at: datetime
    class Config:
        from_attributes = True

class BranchCreate(BaseModel):
    client_id: int
    name: str
    is_main: Optional[bool] = False
    address: Optional[str] = None
    colonia: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    areas: Optional[List[str]] = None


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    is_main: Optional[bool] = None
    address: Optional[str] = None
    colonia: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None


class BranchResponse(BaseModel):
    branch_id: int
    name: str
    is_main: bool
    address: Optional[str]
    colonia: Optional[str]
    zip_code: Optional[str]
    city: Optional[str]
    created_at: datetime
    areas: Optional[List[AreaResponse]] = None

    class Config:
        from_attributes = True

class ClientCreate(BaseModel):
    name: str
    comercial_name: Optional[str] = None
    rfc: Optional[str] = None
    contact_id: Optional[int] = None
    address: Optional[str] = None
    colonia: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    # Campos opcionales para crear contacto automáticamente
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    contact_rol: Optional[str] = None
    branches: Optional[List[BranchCreate]] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    comercial_name: Optional[str] = None
    rfc: Optional[str] = None
    contact_id: Optional[int] = None
    address: Optional[str] = None
    colonia: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    # Campos opcionales para actualizar contacto
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    contact_rol: Optional[str] = None


class ClientResponse(BaseModel):
    client_id: int
    name: str
    comercial_name: Optional[str]
    rfc: Optional[str]
    address: Optional[str]
    colonia: Optional[str]
    zip_code: Optional[str]
    city: Optional[str]
    is_active: bool
    created_at: datetime
    contact: Optional[ContactRead] = None
    branches: Optional[List[BranchResponse]] = None

    class Config:
        from_attributes = True


class ClientListResponse(BaseModel):
    client_id: int
    name: str
    rfc: Optional[str]
    address: Optional[str]
    colonia: Optional[str]
    zip_code: Optional[str]
    city: Optional[str]
    is_active: bool
    total_branches: int
    total_areas: int
    created_at: datetime
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_rol: Optional[str] = None
    class Config:
        from_attributes = True
