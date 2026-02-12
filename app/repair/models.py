from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum, LargeBinary
from core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

class TallerStatus(str, Enum):
    PENDIENTE = "pendiente"
    PAUSADO = "pausado"
    LISTO = "listo"

class TallerLocation(str, Enum):
    ZONA_1 = "zona_1"
    ZONA_2 = "zona_2"
    ZONA_3 = "zona_3"
    ZONA_4 = "zona_4"
    BASURA = "basura"

class TallerProcess(str, Enum):
    DESCONOCIDO = "desconocido"
    PROCESO_1 = "proceso_1"
    PROCESO_2 = "proceso_2"
    PROCESO_3 = "proceso_3"

class TallerEstatus(str, Enum):
    EN_ESPERA_AUTORIZACION = "en_espera_autorizacion"
    EN_ESPERA_PIEZA = "en_espera_pieza"
    PAUSADO = "pausado"
    LISTO = "listo"

class Procedencia(str, Enum):
    BODEGA = "bodega"
    ASIGNADO = "asignado"
    VENDIDO = "vendido"
    DESCONOCIDO = "desconocido"

class Repair(Base):
    __tablename__ = "repairs"

    repair_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False, index=True)
    model = Column(String(255), nullable=False)
    serie = Column(String(255), nullable=False)
    model_toner = Column(String(255), nullable=False)
    
    # Campos específicos del taller
    fecha_alta = Column(DateTime, default=datetime.utcnow, nullable=False)
    procedencia = Column(SQLEnum(Procedencia), nullable=False)
    estado_taller = Column(SQLEnum(TallerStatus), nullable=False, default=TallerStatus.PENDIENTE)
    fecha_conclusion = Column(DateTime, nullable=True)
    folio_escaneado = Column(String(255), nullable=True)  # Ruta del archivo escaneado
    foto_evidencia = Column(String(255), nullable=True)  # Ruta de la foto
    ubicacion = Column(SQLEnum(TallerLocation), nullable=True)
    proceso = Column(SQLEnum(TallerProcess), default=TallerProcess.DESCONOCIDO)
    estatus = Column(SQLEnum(TallerEstatus), nullable=False, default=TallerEstatus.EN_ESPERA_AUTORIZACION)
    diagnostico_inicial = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    equipment = relationship("Equipment", backref="repairs")