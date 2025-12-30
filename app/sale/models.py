from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, DECIMAL
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from enum import Enum


class SaleStatus(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    ENTREGADA = "entregada"
    CANCELADA = "cancelada"


class Sale(Base):
    __tablename__ = "sales"
    
    sale_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False, index=True)
    invoice_number = Column(String(50), unique=True, nullable=True, index=True)
    sale_status = Column(SQLEnum(SaleStatus), nullable=False, default=SaleStatus.PENDIENTE)
    sale_price = Column(DECIMAL(10, 2), nullable=False)
    is_foreign = Column(Boolean, default=False)  
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    
    # Relaciones
    client = relationship("Client", foreign_keys=[client_id])
    branch = relationship("Branch", foreign_keys=[branch_id])
    area = relationship("Area", foreign_keys=[area_id])
    equipment = relationship("Equipment", foreign_keys=[item_id])
    creator = relationship("User", foreign_keys=[created_by])
