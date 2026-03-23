from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import enum


class NotificationType(str, enum.Enum):
    COBRANZA_VENCIDA = "cobranza_vencida"
    COBRANZA_POR_VENCER = "cobranza_por_vencer"
    TICKET_URGENTE = "ticket_urgente"
    COMPRA_PENDIENTE = "compra_pendiente"
    VACACION_PENDIENTE = "vacacion_pendiente"
    RENTA_POR_VENCER = "renta_por_vencer"
    SISTEMA = "sistema"
    INFO = "info"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False, default=NotificationType.INFO)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    link = Column(String(500), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", foreign_keys=[user_id])
