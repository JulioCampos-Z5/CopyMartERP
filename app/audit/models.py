from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    action = Column(String(50), nullable=False)       # create, update, delete, login, logout
    module = Column(String(100), nullable=False)       # clients, sales, rents, etc.
    record_id = Column(Integer, nullable=True)         # ID del registro afectado
    detail = Column(Text, nullable=True)               # Descripción del cambio
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", foreign_keys=[user_id])
