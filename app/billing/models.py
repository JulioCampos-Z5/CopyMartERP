from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, DECIMAL, Date, Text
from sqlalchemy.orm import relationship
from ..core.database import Base
from datetime import datetime
from enum import Enum


class BillingStatus(str, Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    VENCIDO = "vencido"


class BillingType(str, Enum):
    RENTA = "renta"
    VENTA = "venta"


class Billing(Base):
    __tablename__ = "billings"
    
    billing_id = Column(Integer, primary_key=True, index=True)
    billing_type = Column(SQLEnum(BillingType), nullable=False, index=True)
    rent_id = Column(Integer, ForeignKey("rents.rent_id"), nullable=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=True, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    target_date = Column(Date, nullable=False, index=True)  # Fecha objetivo de pago
    due_date = Column(Date, nullable=False, index=True)     # Fecha de vencimiento
    payment_date = Column(Date, nullable=True)               # Fecha de pago real
    status = Column(SQLEnum(BillingStatus), nullable=False, default=BillingStatus.PENDIENTE, index=True)
    follow_up = Column(Boolean, default=False, index=True)  # Requiere seguimiento
    payment_term = Column(Integer, nullable=True)  # Días de crédito (ej: 30, 60, 90)
    payment_day = Column(Integer, nullable=True)   # Día específico del mes para pago (1-31)
    comment = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    
    # Relaciones
    rent = relationship("Rent", foreign_keys=[rent_id])
    sale = relationship("Sale", foreign_keys=[sale_id])
    client = relationship("Client", foreign_keys=[client_id])
    branch = relationship("Branch", foreign_keys=[branch_id])
    area = relationship("Area", foreign_keys=[area_id])
    creator = relationship("User", foreign_keys=[created_by])
