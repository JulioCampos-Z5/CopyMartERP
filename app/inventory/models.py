from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, Text, ForeignKey, Enum as SQLEnum, Table
from core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

from equipment.models import Brand, Supplier, Equipment, TypeColor, LocationStatus

class ColorType(str, Enum):
    K = "k"  # Negro
    C = "c"  # Cyan
    M = "m"  # Magenta
    Y = "y"  # Amarillo

class QualityType(str, Enum):
    ORIGINAL = "original"
    GENERICO = "generico"
    REPARADO = "reparado"
    NUEVA = "nueva"
    USADO = "usado"
    NA = "n/a"

class ItemType(str, Enum):
    TONER = "toner"
    REFACCION = "refaccion"

class SectionLocation(str, Enum):
    SECCION_1 = "seccion_1"
    SECCION_2 = "seccion_2"
    SECCION_3 = "seccion_3"
    SECCION_4 = "seccion_4"
    SECCION_5 = "seccion_5"
    SECCION_6 = "seccion_6"

class ItemCatalog(Base):
    __tablename__ = "item_catalog"
    
    catalog_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), unique=True, nullable=False, index=True)  
    description = Column(Text, nullable=True)
    item_type = Column(SQLEnum(ItemType), nullable=False)  # toner o refaccion
    brand_id = Column(Integer, ForeignKey("brands.brand_id"), nullable=True)
    color = Column(SQLEnum(ColorType), nullable=True)  # Para toners
    usage = Column(Text, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    brand = relationship("Brand", foreign_keys=[brand_id])
    inventory_items = relationship("InventoryItem", back_populates="catalog_item")

class Shelf(Base):
    __tablename__ = "shelves"
    shelf_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    section = Column(SQLEnum(SectionLocation), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    inventory_items = relationship("InventoryItem", back_populates="shelf")

inventory_equipment = Table(
    'inventory_equipment',
    Base.metadata,
    Column('inventory_id', Integer, ForeignKey('inventory.inventory_id'), primary_key=True),
    Column('equipment_id', Integer, ForeignKey('items.item_id'), primary_key=True)
)

class InventoryItem(Base):
    __tablename__ = "inventory"
    
    inventory_id = Column(Integer, primary_key=True, index=True)
    item_code = Column(String(100), unique=True, nullable=False, index=True) 
    catalog_id = Column(Integer, ForeignKey("item_catalog.catalog_id"), nullable=False) 
    section = Column(SQLEnum(SectionLocation), nullable=False)
    shelf_id = Column(Integer, ForeignKey("shelves.shelf_id"), nullable=True)
    quality = Column(SQLEnum(QualityType), nullable=False)
    entry_date = Column(DateTime, default=datetime.utcnow)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=True)
    invoice = Column(String(100), nullable=True)
    cost = Column(DECIMAL(10,2), nullable=True)
    is_available = Column(Boolean, default=True) 
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relaciones
    catalog_item = relationship("ItemCatalog", back_populates="inventory_items")
    supplier = relationship("Supplier", foreign_keys=[supplier_id])
    shelf = relationship("Shelf", back_populates="inventory_items")
    equipments = relationship("Equipment", secondary=inventory_equipment)

class ItemStock(Base):
    __tablename__ = "item_stock"
    
    stock_id = Column(Integer, primary_key=True, index=True)
    catalog_id = Column(Integer, ForeignKey("item_catalog.catalog_id"), unique=True, nullable=False)
    stock_min = Column(Integer, default=0)
    stock_max = Column(Integer, default=0)
    
    # Relación
    catalog_item = relationship("ItemCatalog")

class InventorySequence(Base):
    __tablename__ = "inventory_sequences"
    
    sequence_id = Column(Integer, primary_key=True, index=True)
    prefix = Column(String(10), unique=True, nullable=False)  # TG, TO, RN, RR, RU
    current_value = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)