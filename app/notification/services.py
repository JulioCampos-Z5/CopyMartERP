from sqlalchemy.orm import Session
from sqlalchemy import desc
from notification.models import Notification, NotificationType
from notification.schemas import NotificationCreate
from billing.models import Billing
from ticket.models import Ticket, ReportStatus
from rent.models import Rent
from auth.models import User, RolEnum
from datetime import datetime, timedelta


class NotificationService:

    @staticmethod
    def create(db: Session, data: NotificationCreate) -> Notification:
        notif = Notification(**data.model_dump())
        db.add(notif)
        db.commit()
        db.refresh(notif)
        return notif

    @staticmethod
    def get_user_notifications(db: Session, user_id: int, skip: int = 0,
                                limit: int = 50, unread_only: bool = False):
        query = db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()

    @staticmethod
    def count_unread(db: Session, user_id: int) -> int:
        return db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()

    @staticmethod
    def mark_as_read(db: Session, notification_id: int, user_id: int) -> bool:
        notif = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if notif:
            notif.is_read = True
            db.commit()
            return True
        return False

    @staticmethod
    def mark_all_read(db: Session, user_id: int) -> int:
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).update({"is_read": True})
        db.commit()
        return count

    @staticmethod
    def generate_system_notifications(db: Session):
        """Genera notificaciones automáticas basadas en el estado del sistema."""
        now = datetime.utcnow()
        admins = db.query(User).filter(
            User.rol.in_([RolEnum.ADMINISTRADOR, RolEnum.GERENCIA]),
            User.is_active == True
        ).all()
        admin_ids = [u.user_id for u in admins]

        # Cobranza vencida
        try:
            overdue = db.query(Billing).filter(
                Billing.status == "vencido"
            ).count()
            if overdue > 0:
                for uid in admin_ids:
                    existing = db.query(Notification).filter(
                        Notification.user_id == uid,
                        Notification.type == NotificationType.COBRANZA_VENCIDA,
                        Notification.created_at >= now - timedelta(hours=24)
                    ).first()
                    if not existing:
                        db.add(Notification(
                            user_id=uid,
                            type=NotificationType.COBRANZA_VENCIDA,
                            title=f"{overdue} facturas vencidas",
                            message="Hay facturas pendientes de cobro que ya vencieron.",
                            link="/cobranza"
                        ))
        except Exception:
            pass

        # Tickets urgentes
        try:
            urgent = db.query(Ticket).filter(
                Ticket.report_status == ReportStatus.URGENTE
            ).count()
            if urgent > 0:
                for uid in admin_ids:
                    existing = db.query(Notification).filter(
                        Notification.user_id == uid,
                        Notification.type == NotificationType.TICKET_URGENTE,
                        Notification.created_at >= now - timedelta(hours=24)
                    ).first()
                    if not existing:
                        db.add(Notification(
                            user_id=uid,
                            type=NotificationType.TICKET_URGENTE,
                            title=f"{urgent} tickets urgentes",
                            message="Hay tickets de servicio marcados como urgentes sin atender.",
                            link="/ordenes-servicio"
                        ))
        except Exception:
            pass

        db.commit()
