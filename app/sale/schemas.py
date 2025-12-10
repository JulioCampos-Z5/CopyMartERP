from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum


class SaleStatus(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    ENTREGADA = "entregada"
    CANCELADA = "cancelada"

class ClientBasic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    client_id: int
    name: str
    comercial_name: Optional[str] = None


class BranchBasic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    branch_id: int
    name: str


class AreaBasic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    area_id: int
    name: str


class EquipmentBasic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: int
    sku: Optional[str] = None
    model: str
    serie: str
    brand_id: int

class SaleCreate(BaseModel):
    client_id: int
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    item_id: int
    sale_status: SaleStatus = SaleStatus.PENDIENTE
    sale_price: float = Field(gt=0, description="Precio de venta debe ser mayor a 0")
    is_foreign: bool = False

    @field_validator('area_id')
    def validate_area_assignment(cls, v, values):
        # Si se asigna área sin sucursal, se validará en el servicio
        if v and not values.get('branch_id'):
            pass
        return v

class SaleUpdate(BaseModel):
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    sale_status: Optional[SaleStatus] = None
    sale_price: Optional[float] = Field(None, gt=0)
    is_foreign: Optional[bool] = None
    is_active: Optional[bool] = None

class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_id: int
    client_id: int
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    item_id: int
    invoice_number: Optional[str] = None
    sale_status: SaleStatus
    sale_price: float
    is_foreign: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    client: ClientBasic
    branch: Optional[BranchBasic] = None
    area: Optional[AreaBasic] = None
    equipment: EquipmentBasic


class SaleList(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sale_id: int
    invoice_number: Optional[str] = None
    client_name: str
    branch_name: Optional[str] = None
    area_name: Optional[str] = None
    equipment_model: str
    equipment_serie: str
    sale_status: SaleStatus
    sale_price: float
    is_foreign: bool

class SaleFilter(BaseModel):
    client_id: Optional[int] = None
    branch_id: Optional[int] = None
    area_id: Optional[int] = None
    sale_status: Optional[SaleStatus] = None
    is_foreign: Optional[bool] = None
    is_active: Optional[bool] = True
