from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Text, ForeignKey
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

    stops = relationship("RouteStop", back_populates="route", cascade="all, delete-orphan", order_by="RouteStop.stop_order")


class RouteStop(Base):
    __tablename__ = "route_stops"

    stop_id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.route_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=True)
    stop_order = Column(Integer, nullable=False, default=0)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    visit_status = Column(String(20), nullable=False, default="pendiente")  # pendiente | visitado | no_visitado | reagendado
    no_visit_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    route = relationship("Route", back_populates="stops")
    client = relationship("Client")
    branch = relationship("Branch")
