from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric, Enum as SQLEnum, Boolean
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
    authorized_amount = Column(Integer, nullable=True)
    quality = Column(String(100), nullable=True)
    justification = Column(Text, nullable=True)
    type = Column(SQLEnum(PurchaseType), nullable=False, default=PurchaseType.INTERNA)
    supplier1_name = Column(String(255), nullable=True)
    supplier1_cost = Column(Numeric(10, 2), nullable=True)
    supplier2_name = Column(String(255), nullable=True)
    supplier2_cost = Column(Numeric(10, 2), nullable=True)
    supplier3_name = Column(String(255), nullable=True)
    supplier3_cost = Column(Numeric(10, 2), nullable=True)
    authorized_by_area_chief_id = Column(Integer, ForeignKey("contacts.contact_id"), nullable=True, index=True)
    authorized_by_area_chief_date = Column(DateTime(timezone=True), nullable=True)
    authorized_by_admin_id = Column(Integer, ForeignKey("contacts.contact_id"), nullable=True, index=True)
    authorized_by_admin_date = Column(DateTime(timezone=True), nullable=True)
    quotation_file = Column(String(500), nullable=True)
    supplier_payment_file = Column(String(500), nullable=True)
    supplier_invoice_file = Column(String(500), nullable=True)
    is_paid = Column(Boolean, nullable=True, default=None)
    shipping_method = Column(String(100), nullable=True)
    shipping_cost = Column(Numeric(10, 2), nullable=True)
    shipping_code = Column(String(100), nullable=True, index=True)
    status = Column(SQLEnum(PurchaseStatus), nullable=False, default=PurchaseStatus.EN_CURSO, index=True)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    

    sparepart = relationship("Sparepart", backref="purchases")
    user = relationship("Contact", foreign_keys=[user_id], backref="created_purchases")
    authorized_by_area_chief = relationship("Contact", foreign_keys=[authorized_by_area_chief_id], backref="authorized_as_chief")
    authorized_by_admin = relationship("Contact", foreign_keys=[authorized_by_admin_id], backref="authorized_as_admin")