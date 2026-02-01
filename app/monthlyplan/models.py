from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
import enum

monthlyplan_users = Table(
    'monthlyplan_users',
    Base.metadata,
    Column('monthlyplan_id', Integer, ForeignKey('monthly_plans.monthlyplan_id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True)
)

class AttendanceStatus(str, enum.Enum):
    VISITADO = "visitado"
    NO_QUEDO = "no_quedo"
    PENDIENTE = "pendiente"

class ServiceType(Base):
    __tablename__ = "service_types"
    
    service_type_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacion
    monthly_plans = relationship("MonthlyPlan", back_populates="service_type")

class MonthlyPlan(Base):
    __tablename__ = "monthly_plans"
    
    monthlyplan_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=False)
    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=True)
    ticket_id = Column(Integer, ForeignKey("tickets.ticket_id"), nullable=True)
    
    service_type_id = Column(Integer, ForeignKey("service_types.service_type_id"), nullable=False)
    
    attendance_status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PENDIENTE, nullable=False)
    description = Column(Text, nullable=True)
    visit_date = Column(DateTime, nullable=False)
    
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacion
    client = relationship("Client")
    branch = relationship("Branch")
    area = relationship("Area")
    ticket = relationship("Ticket")
    service_type = relationship("ServiceType", back_populates="monthly_plans")
    creator = relationship("User", foreign_keys=[created_by])
    assigned_users = relationship("User", secondary=monthlyplan_users, backref="monthly_plans")