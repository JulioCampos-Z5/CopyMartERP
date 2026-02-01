from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum, DECIMAL, Date, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from enum import Enum


class ContractStatus(str, Enum):
    PENDIENTE = "pendiente"
    SIN_FIRMAR = "sin_firmar"
    VIGENTE = "vigente"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"


class Rent(Base):
    __tablename__ = "rents"
    
    rent_id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String(50), unique=True, nullable=True, index=True) 
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False, index=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=True, index=True)
    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False, index=True)
    
    rent = Column(DECIMAL(10, 2), nullable=False)
    contract_status = Column(SQLEnum(ContractStatus), nullable=False, default=ContractStatus.PENDIENTE, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_foreign = Column(Boolean, default=False)
    has_print_service = Column(Boolean, default=False, index=True)
    bn_included = Column(Integer, nullable=True, default=0) 
    bn_cost_per_excess = Column(DECIMAL(10, 4), nullable=True, default=0.0)  
    color_included = Column(Integer, nullable=True, default=0)
    color_cost_per_excess = Column(DECIMAL(10, 4), nullable=True, default=0.0)
    print_notes = Column(Text, nullable=True)  
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    
    client = relationship("Client", foreign_keys=[client_id])
    branch = relationship("Branch", foreign_keys=[branch_id])
    area = relationship("Area", foreign_keys=[area_id])
    equipment = relationship("Equipment", foreign_keys=[item_id])
    creator = relationship("User", foreign_keys=[created_by])
    billings = relationship("Billing", back_populates="rent")
    print_counters = relationship("PrintCounter", back_populates="rent", cascade="all, delete-orphan")