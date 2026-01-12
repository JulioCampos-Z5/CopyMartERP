from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from ticket.models import ReportStatus, ReportType

class TicketBase(BaseModel):
    client_id: int
    branch_id: int
    area_id: Optional[int] = None
    report_type: ReportType
    description: str
    evidence: Optional[str] = None
    corrective_action: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    report_status: Optional[ReportStatus] = None
    report_type: Optional[ReportType] = None
    description: Optional[str] = None
    evidence: Optional[str] = None
    corrective_action: Optional[str] = None

class TicketResponse(TicketBase):
    ticket_id: int
    report_status: ReportStatus
    created_by: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TicketListResponse(BaseModel):
    ticket_id: int
    client_id: int
    branch_id: int
    report_status: ReportStatus
    report_type: ReportType
    description: str
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True