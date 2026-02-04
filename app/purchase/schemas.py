from pydantic import BaseModel, Field, ConfigDict, field_validator
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

class SupplierInfo(BaseModel):
    name: str = Field(..., max_length=255, description="Nombre del proveedor")
    cost: Decimal = Field(..., ge=0, description="Costo del proveedor")

class SparepartInPurchase(BaseModel):
    sparepart_id: Optional[int] = None
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
    sparepart_id: Optional[int] = Field(None, description="ID de la refacción")
    user_id: int = Field(..., description="ID del usuario que realiza la compra")
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la compra")
    amount: int = Field(..., ge=1, description="Cantidad solicitada")
    authorized_amount: Optional[int] = Field(None, ge=0, description="Cantidad autorizada")
    quality: Optional[str] = Field(None, max_length=100, description="Calidad")
    justification: Optional[str] = Field(None, description="Justificación de la compra")
    type: PurchaseTypeEnum = Field(default=PurchaseTypeEnum.INTERNA, description="Tipo de compra")
    
    # Proveedores
    supplier1_name: Optional[str] = Field(None, max_length=255, description="Nombre proveedor 1")
    supplier1_cost: Optional[Decimal] = Field(None, ge=0, description="Costo proveedor 1")
    supplier2_name: Optional[str] = Field(None, max_length=255, description="Nombre proveedor 2")
    supplier2_cost: Optional[Decimal] = Field(None, ge=0, description="Costo proveedor 2")
    supplier3_name: Optional[str] = Field(None, max_length=255, description="Nombre proveedor 3")
    supplier3_cost: Optional[Decimal] = Field(None, ge=0, description="Costo proveedor 3")
    
    # Archivos
    quotation_file: Optional[str] = Field(None, max_length=500, description="Ruta archivo cotización")
    supplier_payment_file: Optional[str] = Field(None, max_length=500, description="Ruta archivo pago proveedor")
    supplier_invoice_file: Optional[str] = Field(None, max_length=500, description="Ruta factura proveedor")
    
    # Para ventas
    is_paid: Optional[bool] = Field(None, description="Si es venta, indica si está pagado")
    
    shipping_method: Optional[str] = Field(None, max_length=100, description="Método de envío")
    shipping_cost: Optional[Decimal] = Field(None, ge=0, description="Costo de envío")
    shipping_code: Optional[str] = Field(None, max_length=100, description="Código de rastreo")
    status: PurchaseStatusEnum = Field(default=PurchaseStatusEnum.EN_CURSO, description="Estado de la compra")
    comments: Optional[str] = Field(None, description="Comentarios adicionales")
    end_date: Optional[datetime] = Field(None, description="Fecha de finalización")

    @field_validator('supplier1_name', 'supplier2_name', 'supplier3_name')
    def validate_supplier_name(cls, v, info):
        field_name = info.field_name
        if v is not None:
            cost_field = field_name.replace('name', 'cost')
        return v

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[int] = Field(None, ge=1)
    authorized_amount: Optional[int] = Field(None, ge=0)
    quality: Optional[str] = Field(None, max_length=100)
    justification: Optional[str] = None
    type: Optional[PurchaseTypeEnum] = None
    
    # Proveedores
    supplier1_name: Optional[str] = Field(None, max_length=255)
    supplier1_cost: Optional[Decimal] = Field(None, ge=0)
    supplier2_name: Optional[str] = Field(None, max_length=255)
    supplier2_cost: Optional[Decimal] = Field(None, ge=0)
    supplier3_name: Optional[str] = Field(None, max_length=255)
    supplier3_cost: Optional[Decimal] = Field(None, ge=0)
    
    # Archivos
    quotation_file: Optional[str] = Field(None, max_length=500)
    supplier_payment_file: Optional[str] = Field(None, max_length=500)
    supplier_invoice_file: Optional[str] = Field(None, max_length=500)
    
    # Para ventas
    is_paid: Optional[bool] = None
    
    shipping_method: Optional[str] = Field(None, max_length=100)
    shipping_cost: Optional[Decimal] = Field(None, ge=0)
    shipping_code: Optional[str] = Field(None, max_length=100)
    status: Optional[PurchaseStatusEnum] = None
    comments: Optional[str] = None
    end_date: Optional[datetime] = None

class PurchaseResponse(PurchaseBase):
    purchase_id: int
    authorized_by_area_chief_id: Optional[int] = None
    authorized_by_area_chief_date: Optional[datetime] = None
    authorized_by_admin_id: Optional[int] = None
    authorized_by_admin_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class PurchaseDetailResponse(BaseModel):
    purchase_id: int
    sparepart_id: Optional[int] = None
    user_id: int
    name: str
    amount: int
    authorized_amount: Optional[int] = None
    quality: Optional[str] = None
    justification: Optional[str] = None
    type: PurchaseTypeEnum
    
    # Proveedores
    supplier1_name: Optional[str] = None
    supplier1_cost: Optional[Decimal] = None
    supplier2_name: Optional[str] = None
    supplier2_cost: Optional[Decimal] = None
    supplier3_name: Optional[str] = None
    supplier3_cost: Optional[Decimal] = None
    
    # Autorizaciones
    authorized_by_area_chief_id: Optional[int] = None
    authorized_by_area_chief_date: Optional[datetime] = None
    authorized_by_admin_id: Optional[int] = None
    authorized_by_admin_date: Optional[datetime] = None
    
    # Archivos
    quotation_file: Optional[str] = None
    supplier_payment_file: Optional[str] = None
    supplier_invoice_file: Optional[str] = None
    
    # Para ventas
    is_paid: Optional[bool] = None
    
    shipping_method: Optional[str] = None
    shipping_cost: Optional[Decimal] = None
    shipping_code: Optional[str] = None
    status: PurchaseStatusEnum
    comments: Optional[str] = None
    created_at: datetime
    end_date: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    sparepart: Optional[SparepartInPurchase] = None
    user: UserInPurchase
    authorized_by_area_chief: Optional[UserInPurchase] = None
    authorized_by_admin: Optional[UserInPurchase] = None
    
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

class PurchaseAuthorizationUpdate(BaseModel):
    """Para actualizar autorizaciones"""
    authorized_amount: Optional[int] = Field(None, ge=0, description="Cantidad autorizada")
    comments: Optional[str] = Field(None, description="Comentarios sobre la autorización")

class PurchaseStatsResponse(BaseModel):
    total_purchases: int
    by_status: dict[str, int]
    by_type: dict[str, int]
    total_shipping_cost: Decimal
    pending_authorizations: int
    total_authorized: int