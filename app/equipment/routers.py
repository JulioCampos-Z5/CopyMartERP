""" 
==============================================================================
MÓDULO DE EQUIPOS - ROUTERS
==============================================================================
Endpoints para la gestión de equipos, marcas y proveedores.

Rutas disponibles:
  MARCAS:
    - POST   /brands/           -> Crear nueva marca
    - GET    /brands/           -> Listar todas las marcas
  
  PROVEEDORES:
    - POST   /suppliers/        -> Crear nuevo proveedor
    - GET    /suppliers/        -> Listar todos los proveedores
  
  EQUIPOS:
    - POST   /                  -> Crear nuevo equipo (genera SKU automático)
    - GET    /                  -> Listar todos los equipos
    - GET    /{item_id}         -> Obtener equipo por ID
    - PUT    /{item_id}         -> Actualizar equipo completo
    - PATCH  /{item_id}/status  -> Actualizar solo ubicación del equipo

Actualizado: 3 de diciembre de 2025
==============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.equipment.models import Supplier, Equipment, Brand, LocationStatus
from app.equipment.schemas import (
    BrandCreate, BrandRead, 
    SupplierCreate, SupplierRead, 
    EquipmentCreate, EquipmentRead, EquipmentUpdate, StatusUpdate
)
from app.equipment.services import create_brand, create_supplier, create_equipment, update_equipment_status, update_equipment
from app.core.database import get_db

router = APIRouter()

# ==============================================================================
# ENDPOINTS DE MARCAS
# ==============================================================================

@router.post("/brands/", response_model=BrandRead)
def add_brand(brand: BrandCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva marca de equipos.
    
    Args:
        brand: Datos de la marca (name, prefix)
               - name: Nombre completo de la marca (ej: "Hewlett-Packard")
               - prefix: Prefijo para generar SKU (ej: "HP", máx 5 caracteres)
    
    Returns:
        BrandRead: Marca creada con su ID asignado
    """
    return create_brand(db, brand)

@router.get("/brands/", response_model=List[BrandRead])
def list_brands(db: Session = Depends(get_db)):
    """Retorna todas las marcas registradas en el sistema."""
    return db.query(Brand).all()

# ==============================================================================
# ENDPOINTS DE PROVEEDORES
# ==============================================================================

@router.post("/suppliers/", response_model=SupplierRead)
def add_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo proveedor de equipos.
    
    Args:
        supplier: Datos del proveedor (name)
    
    Returns:
        SupplierRead: Proveedor creado con su ID asignado
    """
    return create_supplier(db, supplier)

@router.get("/suppliers/", response_model=List[SupplierRead])
def list_suppliers(db: Session = Depends(get_db)):
    """Retorna todos los proveedores registrados en el sistema."""
    return db.query(Supplier).all()

# ==============================================================================
# ENDPOINTS DE EQUIPOS
# ==============================================================================

@router.post("/", response_model=EquipmentRead)
def add_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo equipo en el inventario.
    
    El SKU se genera automáticamente usando el prefijo de la marca + número secuencial.
    Ejemplo: Si la marca es "HP" y es el tercer equipo HP, el SKU será "hp03"
    
    Args:
        equipment: Datos del equipo (brand_id, model, serie, etc.)
    
    Returns:
        EquipmentRead: Equipo creado con SKU generado
    
    Raises:
        HTTPException 400: Si la marca no existe
    """
    try:
        return create_equipment(db, equipment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[EquipmentRead])
def list_equipment(db: Session = Depends(get_db)):
    """Retorna todos los equipos del inventario."""
    return db.query(Equipment).all()

@router.get("/{item_id}", response_model=EquipmentRead)
def get_equipment(item_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un equipo específico por su ID.
    
    Args:
        item_id: ID del equipo a buscar
    
    Returns:
        EquipmentRead: Datos del equipo
    
    Raises:
        HTTPException 404: Si el equipo no existe
    """
    equipment = db.query(Equipment).filter(Equipment.item_id == item_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment

@router.put("/{item_id}", response_model=EquipmentRead)
def update_equipment_endpoint(item_id: int, equipment_data: EquipmentCreate, db: Session = Depends(get_db)):
    """
    Actualiza todos los datos de un equipo existente.
    
    NOTA: El SKU no se modifica aunque se cambie la marca.
    
    Args:
        item_id: ID del equipo a actualizar
        equipment_data: Nuevos datos del equipo
    
    Returns:
        EquipmentRead: Equipo actualizado
    
    Raises:
        HTTPException 404: Si el equipo no existe
    """
    try:
        return update_equipment(db, item_id, equipment_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{item_id}/status", response_model=EquipmentRead)
def change_equipment_status(item_id: int, update: StatusUpdate, db: Session = Depends(get_db)):
    """
    Actualiza únicamente la ubicación/estado de un equipo.
    
    Estados válidos: bodega, asignado, vendido, taller, desconocido
    
    Args:
        item_id: ID del equipo
        update: Objeto con location_status
    
    Returns:
        EquipmentRead: Equipo con ubicación actualizada
    
    Raises:
        HTTPException 400: Si no se proporciona el estado
        HTTPException 404: Si el equipo no existe
    """
    if not update.location_status:
        raise HTTPException(status_code=400, detail="Status is required")
    try:
        return update_equipment_status(db, item_id, update.location_status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))