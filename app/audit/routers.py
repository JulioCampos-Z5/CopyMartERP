from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from auth.routers import get_current_user
from auth.models import User
from audit.schemas import AuditLogResponse, AuditLogCreate
from audit.services import AuditService

router = APIRouter(prefix="/audit", tags=["Auditoría"])


@router.get("/", response_model=List[AuditLogResponse])
def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    module: Optional[str] = None,
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AuditService.get_logs(db, skip=skip, limit=limit,
                                 module=module, action=action, user_id=user_id)


@router.get("/count")
def count_audit_logs(
    module: Optional[str] = None,
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {"count": AuditService.count_logs(db, module=module, action=action, user_id=user_id)}


@router.post("/", response_model=AuditLogResponse)
def create_audit_log(
    entry: AuditLogCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ip = request.client.host if request.client else None
    log = AuditService.log(
        db,
        user_id=current_user.user_id,
        action=entry.action,
        module=entry.module,
        record_id=entry.record_id,
        detail=entry.detail,
        ip_address=ip
    )
    return AuditLogResponse(
        id=log.id,
        user_id=log.user_id,
        action=log.action,
        module=log.module,
        record_id=log.record_id,
        detail=log.detail,
        ip_address=log.ip_address,
        created_at=log.created_at,
        user_name=current_user.full_name
    )
