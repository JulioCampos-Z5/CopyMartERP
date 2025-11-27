from pydantic import BaseModel
<<<<<<< HEAD
from typing import List, Optional
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    rfc: Optional[str] = None
    user_id: Optional[int] = None

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    client_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class BranchBase(BaseModel):
    name: str
=======
from typing import Optional, List
from datetime import datetime

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
>>>>>>> develop
    address: Optional[str] = None
    colonia: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None

<<<<<<< HEAD
class BranchCreate(BranchBase):
    client_id: int

class BranchRead(BranchBase):
    branch_id: int
    client_id: int
    created_at: datetime
    class Config:
        orm_mode = True

class AreaBase(BaseModel):
    name: str
    description: Optional[str] = None

class AreaCreate(AreaBase):
    branch_id: int

class AreaRead(AreaBase):
    area_id: int
    branch_id: int
    created_at: datetime
    class Config:
        orm_mode = True
=======

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
    class Config:
        from_attributes = True
>>>>>>> develop
