from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from core.database import Base

class PurchaseType(str, enum.Enum):
    INTERNA = "Interna"
    VENTA = "Venta"

class PurchaseStatus(str, enum.Enum):
    PAUSADO_BACK_ORDERS = "Pausado Back Orders"
    EN_TRANSITO = "En Tránsito"
    SOLICITUD_GUIA_ALMACEN = "Solicitud Guía Almacén"
    FALTA_PAGO_PROVEEDOR = "Falta Pago Proveedor"
    FALTA_FACTURA = "Falta Factura"
    EN_CURSO = "En Curso"
    POR_REVISAR = "Por Revisar"
    FALTA_AUTORIZACION = "Falta Autorización"
    RECHAZADO = "Rechazado"
    FALTA_ORDEN_SERVICIO = "Falta Orden de Servicio"
    CONCLUIDO = "Concluido"

class Purchase(Base):
    __tablename__ = "purchases"
    
    purchase_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sparepart_id = Column(Integer, ForeignKey("spareparts.sparepart_id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("contacts.contact_id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    amount = Column(Integer, nullable=False)
    quality = Column(String(100), nullable=True)
    justification = Column(Text, nullable=True)
    type = Column(SQLEnum(PurchaseType), nullable=False, default=PurchaseType.INTERNA)
    shipping_method = Column(String(100), nullable=True)
    shipping_cost = Column(Numeric(10, 2), nullable=True)
    shipping_code = Column(String(100), nullable=True, index=True)
    status = Column(SQLEnum(PurchaseStatus), nullable=False, default=PurchaseStatus.EN_CURSO, index=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    

    sparepart = relationship("Sparepart", backref="purchases")
    user = relationship("Contact", backref="purchases")
