from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from equipment.models import TypeColor, LocationStatus

class BrandCreate(BaseModel):
    name: str
    prefix: str

class BrandRead(BaseModel):
    brand_id: int
    name: str
    prefix: str

    class Config:
        from_attributes = True

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    prefix: Optional[str] = None

# SUPPLIER SCHEMAS
class SupplierCreate(BaseModel):
    name: str

class SupplierRead(BaseModel):
    supplier_id: int
    name: str

    class Config:
        from_attributes = True

class SupplierUpdate(BaseModel):
    name: Optional[str] = None

class EquipmentCreate(BaseModel):
    brand_id: int
    model: str
    serie: str
    model_toner: str
    type: TypeColor
    supplier_id: int
    invoice: Optional[str] = None
    cost: Optional[Decimal] = None
    location_status: LocationStatus = LocationStatus.BODEGA
    comments: Optional[str] = None
    is_active: bool = True

class EquipmentRead(BaseModel):
    item_id: int
    sku: Optional[str] = None
    brand_id: int
    model: str
    serie: str
    model_toner: str
    type: TypeColor
    supplier_id: int
    invoice: Optional[str] = None
    cost: Optional[Decimal] = None
    location_status: LocationStatus
    comments: Optional[str] = None
    created_at: datetime
    is_active: bool
    brand: BrandRead
    supplier: SupplierRead

    class Config:
        from_attributes = True

class EquipmentUpdate(BaseModel):
    location_status: Optional[LocationStatus] = None

class EquipmentUpdateFull(BaseModel):
    model: Optional[str] = None
    serie: Optional[str] = None
    model_toner: Optional[str] = None
    type: Optional[TypeColor] = None
    supplier_id: Optional[int] = None
    invoice: Optional[str] = None
    cost: Optional[Decimal] = None
    location_status: Optional[LocationStatus] = None
    comments: Optional[str] = None
    is_active: Optional[bool] = None