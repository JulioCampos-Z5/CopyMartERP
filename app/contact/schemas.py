from pydantic import BaseModel
from datetime import datetime

class ContactBase(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    company: str | None = None
    rol: str | None = None
    is_client: bool | None = True


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    company: str | None = None
    rol: str | None = None
    is_client: bool | None = None
    is_active: bool | None = None


class ContactRead(ContactBase):
    contact_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attibutes: True 