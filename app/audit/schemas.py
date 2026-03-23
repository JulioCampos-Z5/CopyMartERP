from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AuditLogCreate(BaseModel):
    action: str
    module: str
    record_id: Optional[int] = None
    detail: Optional[str] = None


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    module: str
    record_id: Optional[int] = None
    detail: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    user_name: Optional[str] = None

    class Config:
        from_attributes = True
