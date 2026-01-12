from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import enum

class ReportStatus(str, enum.Enum):
    PENDIENTE = "pendiente"
    LISTO = "listo"
    URGENTE = "urgente"
    PROGRAMADO = "programado"
    INFORMATIVO = "informativo"
    NO_QUEDO_VISITA = "no_quedo_en_la_visita"
    ATENCION = "atencion"

class ReportType(str, enum.Enum):
    CONECTIVIDAD = "conectividad"
    ATASCO = "atasco"
    TONER = "toner"
    QUEJAS = "quejas"
    COPIA = "copia"
    RUIDOS = "ruidos"
    IMPRESION = "impresion"
    OTROS = "otros"

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), nullable=False)
    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=True)
    report_status = Column(Enum(ReportStatus), default=ReportStatus.PENDIENTE, nullable=False)
    report_type = Column(Enum(ReportType), nullable=False)
    description = Column(Text, nullable=False)
    evidence = Column(String(500), nullable=True)
    corrective_action = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # relacion
    client = relationship("Client")
    branch = relationship("Branch")
    area = relationship("Area")
    creator = relationship("User", foreign_keys=[created_by])