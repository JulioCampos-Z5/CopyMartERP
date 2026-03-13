from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from notification.schemas import NotificationResponse
from notification.services import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notificaciones"])


@router.get("/", response_model=List[NotificationResponse])
def get_my_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return NotificationService.get_user_notifications(
        db, current_user.user_id, skip=skip, limit=limit, unread_only=unread_only
    )


@router.get("/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {"count": NotificationService.count_unread(db, current_user.user_id)}


@router.put("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = NotificationService.mark_as_read(db, notification_id, current_user.user_id)
    return {"success": success}


@router.put("/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    count = NotificationService.mark_all_read(db, current_user.user_id)
    return {"marked": count}


@router.post("/generate")
def generate_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    NotificationService.generate_system_notifications(db)
    return {"status": "ok"}
