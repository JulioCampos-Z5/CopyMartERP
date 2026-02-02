from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

# Enums - Valores en MAYÚSCULAS para coincidir con la base de datos
class ColorType(str, Enum):
    K = "K"
    C = "C"
    M = "M"
    Y = "Y"

class QualityType(str, Enum):
    ORIGINAL = "ORIGINAL"
    GENERICO = "GENERICO"
    REPARADO = "REPARADO"
    NUEVA = "NUEVA"
    USADO = "USADO"
    NA = "NA"

class ItemType(str, Enum):
    TONER = "TONER"
    REFACCION = "REFACCION"

class SectionLocation(str, Enum):
    SECCION_1 = "SECCION_1"
    SECCION_2 = "SECCION_2"
    SECCION_3 = "SECCION_3"
    SECCION_4 = "SECCION_4"
    SECCION_5 = "SECCION_5"
    SECCION_6 = "SECCION_6"

class ShelfBase(BaseModel):
    name: str
    section: SectionLocation
    description: Optional[str] = None

class ShelfCreate(ShelfBase):
    pass

class ShelfUpdate(BaseModel):
    name: Optional[str] = None
    section: Optional[SectionLocation] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ShelfResponse(ShelfBase):
    shelf_id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class EquipmentSimple(BaseModel):
    item_id: int
    model: str
    serie: str
    
    class Config:
        from_attributes = True

class BrandSimple(BaseModel):
    brand_id: int
    name: str
    prefix: str
    
    class Config:
        from_attributes = True

class SupplierSimple(BaseModel):
    supplier_id: int
    name: str
    
    class Config:
        from_attributes = True


class ItemCatalogBase(BaseModel):
    item_name: str  
    description: Optional[str] = None
    item_type: ItemType
    brand_id: Optional[int] = None
    color: Optional[ColorType] = None
    usage: Optional[str] = None

class ItemCatalogCreate(ItemCatalogBase):
    stock_min: int = 0
    stock_max: int = 0
    
    @validator('stock_max')
    def validate_stock_max(cls, v, values):
        if 'stock_min' in values and v < values['stock_min']:
            raise ValueError('stock_max debe ser mayor o igual a stock_min')
        return v

class ItemCatalogUpdate(BaseModel):
    item_name: Optional[str] = None
    description: Optional[str] = None
    item_type: Optional[ItemType] = None
    brand_id: Optional[int] = None
    color: Optional[ColorType] = None
    usage: Optional[str] = None
    is_active: Optional[bool] = None

class ItemCatalogResponse(ItemCatalogBase):
    catalog_id: int
    created_at: datetime
    is_active: bool
    brand: Optional[BrandSimple] = None
    total_items: int = 0  # Total de items en inventario
    available_items: int = 0  # Items disponibles
    stock_min: int = 0
    stock_max: int = 0
    
    class Config:
        from_attributes = True


class InventoryItemBase(BaseModel):
    catalog_id: int  
    section: SectionLocation
    shelf_id: Optional[int] = None
    quality: QualityType
    supplier_id: Optional[int] = None
    invoice: Optional[str] = None
    cost: Optional[Decimal] = None
    is_available: bool = True
    comments: Optional[str] = None

class InventoryItemCreate(InventoryItemBase):
    equipment_ids: Optional[List[int]] = []  

class InventoryItemUpdate(BaseModel):
    catalog_id: Optional[int] = None
    section: Optional[SectionLocation] = None
    shelf_id: Optional[int] = None
    quality: Optional[QualityType] = None
    supplier_id: Optional[int] = None
    invoice: Optional[str] = None
    cost: Optional[Decimal] = None
    is_available: Optional[bool] = None
    comments: Optional[str] = None
    equipment_ids: Optional[List[int]] = None
    is_active: Optional[bool] = None

class InventoryItemResponse(InventoryItemBase):
    inventory_id: int
    item_code: str  # TG-0001, TO-0002, RN-0003, etc.
    entry_date: datetime
    created_at: datetime
    updated_at: datetime
    is_active: bool
    
    # Relaciones
    catalog_item: Optional[ItemCatalogResponse] = None
    supplier: Optional[SupplierSimple] = None
    shelf: Optional[ShelfResponse] = None
    equipments: List[EquipmentSimple] = []
    
    class Config:
        from_attributes = True

class BulkInventoryCreate(BaseModel):
    catalog_id: int
    quantity: int = Field(..., gt=0, description="Cantidad de items a crear")
    section: SectionLocation
    shelf_id: Optional[int] = None
    quality: QualityType
    supplier_id: Optional[int] = None
    invoice: Optional[str] = None
    cost: Optional[Decimal] = None
    comments: Optional[str] = None
    equipment_ids: Optional[List[int]] = []

# Schema para filtros de búsqueda
class InventoryFilter(BaseModel):
    catalog_id: Optional[int] = None  
    item_name: Optional[str] = None  
    item_type: Optional[ItemType] = None
    section: Optional[SectionLocation] = None
    brand_id: Optional[int] = None
    quality: Optional[QualityType] = None
    color: Optional[ColorType] = None
    shelf_id: Optional[int] = None
    supplier_id: Optional[int] = None
    is_available: Optional[bool] = None
    is_active: Optional[bool] = True
    low_stock: Optional[bool] = None 
    search: Optional[str] = None 

# Schema para estadísticas
class InventoryStats(BaseModel):
    total_catalog_items: int 
    total_inventory_items: int 
    total_toners: int
    total_refacciones: int
    available_items: int 
    low_stock_items: int
    items_by_section: dict
    items_by_quality: dict
    total_value: Decimal

class StockUpdate(BaseModel):
    stock_min: Optional[int] = None
    stock_max: Optional[int] = None
    
    @validator('stock_min', 'stock_max')
    def validate_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v