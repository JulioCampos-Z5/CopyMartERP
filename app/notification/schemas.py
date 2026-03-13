from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from notification.models import NotificationType


class NotificationCreate(BaseModel):
    user_id: int
    type: NotificationType = NotificationType.INFO
    title: str
    message: Optional[str] = None
    link: Optional[str] = None


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    title: str
    message: Optional[str] = None
    link: Optional[str] = None
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
