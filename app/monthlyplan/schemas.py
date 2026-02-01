from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from monthlyplan.models import AttendanceStatus

class ServiceTypeBase(BaseModel):
    name: str
    description: Optional[str] = None

class ServiceTypeCreate(ServiceTypeBase):
    pass

class ServiceTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[int] = None

class ServiceTypeResponse(ServiceTypeBase):
    service_type_id: int
    is_active: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class MonthlyPlanBase(BaseModel):
    client_id: int
    branch_id: int
    area_id: Optional[int] = None
    ticket_id: Optional[int] = None
    service_type_id: int
    description: Optional[str] = None
    visit_date: datetime
    assigned_user_ids: List[int] = Field(default_factory=list)

class MonthlyPlanCreate(MonthlyPlanBase):
    pass

class MonthlyPlanUpdate(BaseModel):
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    ticket_id: Optional[int] = None
    service_type_id: Optional[int] = None
    attendance_status: Optional[AttendanceStatus] = None
    description: Optional[str] = None
    visit_date: Optional[datetime] = None
    assigned_user_ids: Optional[List[int]] = None

class UserBasicInfo(BaseModel):
    user_id: int
    username: str
    email: Optional[str] = None
    
    class Config:
        from_attributes = True

class MonthlyPlanResponse(MonthlyPlanBase):
    monthlyplan_id: int
    attendance_status: AttendanceStatus
    created_by: int
    created_at: datetime
    updated_at: datetime
    assigned_users: List[UserBasicInfo] = []
    
    class Config:
        from_attributes = True

class MonthlyPlanListResponse(BaseModel):
    monthlyplan_id: int
    client_id: int
    branch_id: int
    service_type_id: int
    attendance_status: AttendanceStatus
    visit_date: datetime
    created_at: datetime
    assigned_users: List[UserBasicInfo] = []
    
    class Config:
        from_attributes = True