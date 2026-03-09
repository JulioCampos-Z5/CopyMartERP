from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from enum import Enum


class RouteStatus(str, Enum):
    PROGRAMADA = "programada"
    EN_RUTA = "en_ruta"
    PAUSADA = "pausada"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class Route(Base):
    __tablename__ = "routes"
    
    route_id = Column(Integer, primary_key=True, index=True)
    route_code = Column(String(50), unique=True, nullable=False, index=True)
    driver_name = Column(String(200), nullable=False)
    vehicle = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default=RouteStatus.PROGRAMADA)
    scheduled_date = Column(Date, nullable=False)
    total_stops = Column(Integer, nullable=False, default=0)
    completed_stops = Column(Integer, nullable=False, default=0)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
