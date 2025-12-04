"""
==============================================================================
MÓDULO DE EQUIPOS - SCHEMAS
==============================================================================
Esquemas Pydantic para validación de datos de equipos, marcas y proveedores.

Enums:
  - TypeColor: Tipos de equipo (monocromo, color)
  - LocationStatus: Estados/ubicaciones del equipo

Schemas:
  - BrandCreate/BrandRead: Para marcas
  - SupplierCreate/SupplierRead: Para proveedores
  - EquipmentCreate/EquipmentRead: Para equipos
  - StatusUpdate: Para cambios de ubicación

Actualizado: 3 de diciembre de 2025
==============================================================================
"""

from pydantic import BaseModel
from enum import Enum
from typing import Optional


# ==============================================================================
# ENUMS
# ==============================================================================

class TypeColor(str, Enum):
    """Tipo de impresión del equipo."""
    MONOCROMO = "monocromo"  # Solo blanco y negro
    COLOR = "color"          # Impresión a color


class LocationStatus(str, Enum):
    """
    Estado/ubicación actual del equipo.
    
    - BODEGA: Almacenado en inventario, disponible
    - ASIGNADO: Instalado en cliente (renta o venta)
    - VENDIDO: Vendido al cliente
    - TALLER: En reparación o mantenimiento
    - DESCONOCIDO: Ubicación no determinada
    """
    BODEGA = "bodega"
    ASIGNADO = "asignado"
    VENDIDO = "vendido"
    TALLER = "taller"
    DESCONOCIDO = "desconocido"


# ==============================================================================
# SCHEMAS DE MARCAS
# ==============================================================================

class BrandCreate(BaseModel):
    """
    Schema para crear una nueva marca.
    
    Campos:
        name: Nombre completo de la marca (ej: "Hewlett-Packard")
        prefix: Prefijo para generar SKU (ej: "HP", máximo 5 caracteres)
    """
    name: str
    prefix: str


class BrandRead(BaseModel):
    """Schema de respuesta para marcas."""
    brand_id: int
    name: str
    prefix: str

    class Config:
        orm_mode = True


# ==============================================================================
# SCHEMAS DE PROVEEDORES
# ==============================================================================

class SupplierCreate(BaseModel):
    """
    Schema para crear un nuevo proveedor.
    
    Campos:
        name: Nombre del proveedor/empresa
    """
    name: str


class SupplierRead(BaseModel):
    """Schema de respuesta para proveedores."""
    supplier_id: int
    name: str

    class Config:
        orm_mode = True


# ==============================================================================
# SCHEMAS DE EQUIPOS
# ==============================================================================

class EquipmentCreate(BaseModel):
    """
    Schema para crear un nuevo equipo.
    
    Campos requeridos:
        brand_id: ID de la marca
        model: Modelo del equipo (ej: "LaserJet Pro M404n")
        serie: Número de serie único del equipo
        model_toner: Modelo del tóner compatible (ej: "CF258A")
        type: Tipo de equipo (monocromo/color)
        supplier_id: ID del proveedor
        location_status: Ubicación inicial (generalmente "bodega")
    
    Campos opcionales:
        invoice: Número de factura de compra
        cost: Costo de adquisición
        comments: Notas adicionales
        is_active: Estado activo (default: True)
    """
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
    """Schema de respuesta para equipos (incluye SKU generado)."""
    item_id: int
    sku: str  # SKU generado automáticamente
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
        orm_mode = True


class EquipmentUpdate(BaseModel):
    """Schema para actualizar solo la ubicación (deprecado, usar StatusUpdate)."""
    location_status: LocationStatus


class StatusUpdate(BaseModel):
    """
    Schema para actualizar la ubicación de un equipo.
    
    Usado en el endpoint PATCH /{item_id}/status
    """
    location_status: str