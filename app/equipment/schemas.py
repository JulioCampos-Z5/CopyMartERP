from pydantic import BaseModel
from enum import Enum
from typing import Optional

class TypeColor(str, Enum):
    MONOCROMO = "monocromo"
    COLOR = "color"

class LocationStatus(str, Enum):
    BODEGA = "bodega"
    ASIGNADO = "asignado"
    VENDIDO = "vendido"
    TALLER = "taller"
    DESCONOCIDO = "desconocido"

class BrandCreate(BaseModel):
    name: str
    prefix: str

class BrandRead(BaseModel):
    brand_id: int
    name: str
    prefix: str

    class Config:
        orm_mode = True

class SupplierCreate(BaseModel):
    name: str

class SupplierRead(BaseModel):
    supplier_id: int
    name: str

    class Config:
        orm_mode = True

class EquipmentCreate(BaseModel):
    brand_id: int
    model: str
    serie: str
    model_toner: str
    type: TypeColor
    supplier_id: int
    invoice: Optional[str] = None
    cost: Optional[float] = None
    location_status: LocationStatus
    comments: Optional[str] = None
    is_active: bool = True

class EquipmentRead(BaseModel):
    item_id: int
    sku: Optional[str] = None
    brand_id: int
    brand: Optional[BrandRead] = None
    model: str
    serie: str
    model_toner: str
    type: TypeColor
    supplier_id: int
    supplier: Optional[SupplierRead] = None
    invoice: Optional[str]
    cost: Optional[float]
    location_status: LocationStatus
    comments: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True

class EquipmentUpdate(BaseModel):
    brand_id: Optional[int] = None
    model: Optional[str] = None
    serie: Optional[str] = None
    model_toner: Optional[str] = None
    type: Optional[TypeColor] = None
    supplier_id: Optional[int] = None
    invoice: Optional[str] = None
    cost: Optional[float] = None
    location_status: Optional[LocationStatus] = None
    comments: Optional[str] = None
    is_active: Optional[bool] = None