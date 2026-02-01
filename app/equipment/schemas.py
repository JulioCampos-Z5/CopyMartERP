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
        from_attributes = True

class SupplierCreate(BaseModel):
    name: str

class SupplierRead(BaseModel):
    supplier_id: int
    name: str

    class Config:
        from_attributes = True

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
    sku: Optional[str]
    brand_id: int
    model: str
    serie: str
    model_toner: str
    type: TypeColor
    supplier_id: int
    invoice: Optional[str]
    cost: Optional[float]
    location_status: LocationStatus
    comments: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

class EquipmentUpdate(BaseModel):
    location_status: LocationStatus