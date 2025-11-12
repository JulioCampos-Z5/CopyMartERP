from pydantic import BaseModel
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
    address: Optional[str] = None
    colonia: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None

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