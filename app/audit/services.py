from sqlalchemy.orm import Session
from sqlalchemy import desc
from audit.models import AuditLog
from auth.models import User
from typing import Optional


class AuditService:

    @staticmethod
    def log(db: Session, user_id: Optional[int], action: str, module: str,
            record_id: Optional[int] = None, detail: Optional[str] = None,
            ip_address: Optional[str] = None) -> AuditLog:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            module=module,
            record_id=record_id,
            detail=detail,
            ip_address=ip_address
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def get_logs(db: Session, skip: int = 0, limit: int = 100,
                 module: Optional[str] = None, action: Optional[str] = None,
                 user_id: Optional[int] = None):
        query = db.query(
            AuditLog.id,
            AuditLog.user_id,
            AuditLog.action,
            AuditLog.module,
            AuditLog.record_id,
            AuditLog.detail,
            AuditLog.ip_address,
            AuditLog.created_at,
            User.full_name.label("user_name")
        ).outerjoin(User, AuditLog.user_id == User.user_id)

        if module:
            query = query.filter(AuditLog.module == module)
        if action:
            query = query.filter(AuditLog.action == action)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)

        return query.order_by(desc(AuditLog.created_at)).offset(skip).limit(limit).all()

    @staticmethod
    def count_logs(db: Session, module: Optional[str] = None,
                   action: Optional[str] = None, user_id: Optional[int] = None) -> int:
        query = db.query(AuditLog)
        if module:
            query = query.filter(AuditLog.module == module)
        if action:
            query = query.filter(AuditLog.action == action)
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)
        return query.count()
