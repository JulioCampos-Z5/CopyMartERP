from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, Text, ForeignKey, Enum as SQLEnum
from app.core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

class TypeColor(str, Enum):
    MONOCROMO = "monocromo"
    COLOR = "color"

class LocationStatus(str, Enum):
    BODEGA = "bodega"
    ASIGNADO = "asignado"
    VENDIDO = "vendido"
    TALLER = "taller"
    DESCONOCIDO = "desconocido"

class Brand(Base):
    __tablename__ = "brands"
    brand_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    prefix = Column(String, nullable=False)
    equipments = relationship("Equipment", back_populates="brand")

class Supplier(Base): 
    __tablename__ = "suppliers"
    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    equipments = relationship("Equipment", back_populates="supplier")

class Equipment(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, index=True)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"), index=True)
    model = Column(String, nullable=False)
    serie = Column(String, unique=True, nullable=False)
    model_toner = Column(String, nullable=False)
    type = Column(SQLEnum(TypeColor), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), index=True)
    invoice = Column(String, nullable=True)
    cost = Column(DECIMAL(10,2), nullable=True)
    location_status = Column(SQLEnum(LocationStatus), nullable=False, default=LocationStatus.BODEGA)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    supplier = relationship("Supplier", back_populates="equipments")
    brand = relationship("Brand", back_populates="equipments")