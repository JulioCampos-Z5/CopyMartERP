from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

# Enums
class PurchaseTypeEnum(str, Enum):
    INTERNA = "Interna"
    VENTA = "Venta"

class PurchaseStatusEnum(str, Enum):
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

class SparepartInPurchase(BaseModel):
    sparepart_id: int
    name: str
    code: Optional[str] = None
    brand: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class UserInPurchase(BaseModel):
    contact_id: int
    name: str
    email: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class PurchaseBase(BaseModel):
    sparepart_id: int = Field(..., description="ID de la refacción")
    user_id: int = Field(..., description="ID del usuario que realiza la compra")
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la compra")
    amount: int = Field(..., ge=1, description="Cantidad")
    quality: Optional[str] = Field(None, max_length=100, description="Calidad")
    justification: Optional[str] = Field(None, description="Justificación de la compra")
    type: PurchaseTypeEnum = Field(default=PurchaseTypeEnum.INTERNA, description="Tipo de compra")
    shipping_method: Optional[str] = Field(None, max_length=100, description="Método de envío")
    shipping_cost: Optional[Decimal] = Field(None, ge=0, description="Costo de envío")
    shipping_code: Optional[str] = Field(None, max_length=100, description="Código de rastreo")
    status: PurchaseStatusEnum = Field(default=PurchaseStatusEnum.EN_CURSO, description="Estado de la compra")
    comments: Optional[str] = Field(None, description="Comentarios adicionales")
    end_date: Optional[datetime] = Field(None, description="Fecha de finalización")

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[int] = Field(None, ge=1)
    quality: Optional[str] = Field(None, max_length=100)
    justification: Optional[str] = None
    type: Optional[PurchaseTypeEnum] = None
    shipping_method: Optional[str] = Field(None, max_length=100)
    shipping_cost: Optional[Decimal] = Field(None, ge=0)
    shipping_code: Optional[str] = Field(None, max_length=100)
    status: Optional[PurchaseStatusEnum] = None
    comments: Optional[str] = None
    end_date: Optional[datetime] = None

class PurchaseResponse(PurchaseBase):
    purchase_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class PurchaseDetailResponse(BaseModel):
    purchase_id: int
    sparepart_id: int
    user_id: int
    name: str
    amount: int
    quality: Optional[str] = None
    justification: Optional[str] = None
    type: PurchaseTypeEnum
    shipping_method: Optional[str] = None
    shipping_cost: Optional[Decimal] = None
    shipping_code: Optional[str] = None
    status: PurchaseStatusEnum
    comments: Optional[str] = None
    created_at: datetime
    end_date: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    sparepart: SparepartInPurchase
    user: UserInPurchase
    
    model_config = ConfigDict(from_attributes=True)

class PurchaseListResponse(BaseModel):
    total: int
    items: list[PurchaseDetailResponse]
    page: int
    page_size: int
    total_pages: int

class PurchaseStatusUpdate(BaseModel):
    status: PurchaseStatusEnum
    comments: Optional[str] = Field(None, description="Comentarios sobre el cambio de estado")
    end_date: Optional[datetime] = Field(None, description="Fecha de finalización (si aplica)")

class PurchaseStatsResponse(BaseModel):
    total_purchases: int
    by_status: dict[str, int]
    by_type: dict[str, int]
    total_shipping_cost: Decimal